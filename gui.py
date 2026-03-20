#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GUI 界面模块"""
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from typing import List

from config import load_config, save_config, DEFAULT_EXTENSIONS, PRESET_EXTENSIONS, generate_fake_hex
from utils import calculate_file_hash
from obfuscator import Obfuscator
from restorer import Restorer


class ZipCloakGUI:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        self.root.title("ZipCloak - ZIP 文件混淆工具")
        self.root.geometry("800x700")
        self.root.minsize(750, 650)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.obfuscate_frame = ttk.Frame(self.notebook)
        self.restore_frame = ttk.Frame(self.notebook)
        self.my_frame = ttk.Frame(self.notebook)
        self.LICENSE_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.obfuscate_frame, text='🔒 混淆模式')
        self.notebook.add(self.restore_frame, text='🔓 恢复模式')
        self.notebook.add(self.my_frame, text='关于此软件')
        self.notebook.add(self.LICENSE_frame, text='LICENSE | 开源协议')


        self.setup_obfuscate_tab()
        self.setup_restore_tab()
        self.setup_my_tab()
        self.setup_LICENSE_tab()

        self.status_var = tk.StringVar(value="就绪 | 选择模式开始操作")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief='sunken', anchor='w')
        status_bar.pack(fill='x', side='bottom')
        
        self.load_last_config()

    def setup_obfuscate_tab(self):
        frame = self.obfuscate_frame
        
        ttk.Label(frame, text="📁 源文件夹:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.obf_source_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.obf_source_var, width=55).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=self.browse_obf_source).grid(row=0, column=2, padx=5)
        
        ttk.Label(frame, text="📦 输出 ZIP:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.obf_output_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.obf_output_var, width=55).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="保存为...", command=self.save_obf_output).grid(row=1, column=2, padx=5)
        
        ttk.Label(frame, text="🎯 混淆后缀:").grid(row=2, column=0, sticky='nw', padx=5, pady=5)
        suffix_frame = ttk.Frame(frame)
        suffix_frame.grid(row=2, column=1, columnspan=2, sticky='w')
        
        self.obf_preset_vars = {}
        preset_frame = ttk.Frame(suffix_frame)
        preset_frame.pack(fill='x', pady=2)
        for i, ext in enumerate(PRESET_EXTENSIONS):
            var = tk.BooleanVar(value=True)
            self.obf_preset_vars[ext] = var
            chk = ttk.Checkbutton(preset_frame, text=ext, variable=var, width=8)
            chk.pack(side='left', padx=2)
            if i % 6 == 5:
                preset_frame = ttk.Frame(suffix_frame)
                preset_frame.pack(fill='x', pady=2)
        
        custom_frame = ttk.Frame(suffix_frame)
        custom_frame.pack(fill='x', pady=5)
        ttk.Label(custom_frame, text="自定义:").pack(side='left')
        self.obf_custom_var = tk.StringVar()
        ttk.Entry(custom_frame, textvariable=self.obf_custom_var, width=15).pack(side='left', padx=5)
        ttk.Button(custom_frame, text="添加", command=self.add_obf_custom).pack(side='left', padx=2)
        ttk.Button(custom_frame, text="全选", command=self.select_all_obf).pack(side='left', padx=10)
        ttk.Button(custom_frame, text="清空", command=self.clear_all_obf).pack(side='left')
        
        self.obf_compress_var = tk.BooleanVar(value=self.config.get('compress', True))
        ttk.Checkbutton(frame, text="🗜️ 启用压缩", variable=self.obf_compress_var).grid(row=3, column=0, sticky='w', padx=5, pady=10)
        
        self.obf_progress = ttk.Progressbar(frame, mode='determinate', length=500)
        self.obf_progress.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="▶ 开始混淆", command=self.start_obfuscate).pack(side='left', padx=10)
        
        ttk.Label(frame, text="📜 运行日志:").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.obf_log = scrolledtext.ScrolledText(frame, height=15, width=90)
        self.obf_log.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
        frame.columnconfigure(1, weight=1)

    def setup_restore_tab(self):
        frame = self.restore_frame
        
        ttk.Label(frame, text="📥 混淆 ZIP:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.rst_input_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.rst_input_var, width=55).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=self.browse_rst_input).grid(row=0, column=2, padx=5)
        
        ttk.Label(frame, text="📤 输出目录:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.rst_output_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.rst_output_var, width=55).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="选择...", command=self.select_rst_output).grid(row=1, column=2, padx=5)
        
        ttk.Label(frame, text="🎯 恢复后缀:").grid(row=2, column=0, sticky='nw', padx=5, pady=5)
        suffix_frame = ttk.Frame(frame)
        suffix_frame.grid(row=2, column=1, columnspan=2, sticky='w')
        
        self.rst_preset_vars = {}
        preset_frame = ttk.Frame(suffix_frame)
        preset_frame.pack(fill='x', pady=2)
        for i, ext in enumerate(PRESET_EXTENSIONS):
            var = tk.BooleanVar(value=True)
            self.rst_preset_vars[ext] = var
            chk = ttk.Checkbutton(preset_frame, text=ext, variable=var, width=8)
            chk.pack(side='left', padx=2)
            if i % 6 == 5:
                preset_frame = ttk.Frame(suffix_frame)
                preset_frame.pack(fill='x', pady=2)
        
        custom_frame = ttk.Frame(suffix_frame)
        custom_frame.pack(fill='x', pady=5)
        ttk.Label(custom_frame, text="自定义:").pack(side='left')
        self.rst_custom_var = tk.StringVar()
        ttk.Entry(custom_frame, textvariable=self.rst_custom_var, width=15).pack(side='left', padx=5)
        ttk.Button(custom_frame, text="添加", command=self.add_rst_custom).pack(side='left', padx=2)
        ttk.Button(custom_frame, text="全选", command=self.select_all_rst).pack(side='left', padx=10)
        ttk.Button(custom_frame, text="清空", command=self.clear_all_rst).pack(side='left')
        
        self.rst_progress = ttk.Progressbar(frame, mode='determinate', length=500)
        self.rst_progress.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="▶ 开始恢复", command=self.start_restore).pack(side='left', padx=10)
        
        ttk.Label(frame, text="📜 运行日志:").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        self.rst_log = scrolledtext.ScrolledText(frame, height=15, width=90)
        self.rst_log.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
        frame.columnconfigure(1, weight=1)

    def setup_my_tab(self):
        frame = self.my_frame
        about_text = """
关于此软件 |  版权所属:coralhymn
ZipCloak - zip文件混淆工具
"""
        about_label = tk.Label(
            frame, 
            text=about_text, 
            justify='center',
            font=('Microsoft YaHei UI', 10),
            anchor='w'
        )
        about_label.pack(fill='both', expand=True, padx=20, pady=20)
        
        about2_text = """
ZipCloak - zip文件混淆工具


访问官网:https://coralhymn.com
源码地址:https://github.com/coralhymn/ZipCloak
版权所属:coralhymn | 琴海奶油
开源协议:GPL-2.0

当前版本:1.0.0
功能：对指定类型的文件进行混淆处理，使得某个文件被系统认为是文件夹

使用说明：
[混淆模式]
1. 在【混淆】选项卡中选择源文件夹和输出zip文件位置与设置名称
2. 选择需要混淆的文件扩展名
3. 点击开始混淆生成加密的 ZIP 文件
[恢复模式]
1. 在【恢复】选项卡中选择混淆后的 ZIP 文件
2. 设置输出目录并点击开始恢复（请不要选择根目录，建议自行创建一个子目录）
[配置文件]
在首次运行时，会在软件根目录自动生成一个配置文件zipcloak_config.json，请勿随意删除此文件，此文件将保存您的配置信息，下次运行时将自动读取此文件
您在[混淆模式]中添加的文件扩展名将保存在配置文件中，若需要删除您添加的文件扩展名请删除该文件即可（也可以对json文件进行修改）

本项目基于我的个人项目[https://github.com/CoralHymn/RWMP2_Decryptor]的基础上进行修改
若您是需要对[RWMP2]加密的文件进行解密请勿使用此工具，请使用上方的专属版本
若您对此项目感兴趣不妨在GitHub跟我点一颗Star，这对我的动力将是无比强大

注意事项：
请勿使用此工具对重要文件进行混淆处理、本人对产生的损失不负任何责任
本人未进行深度测试，在使用此工具时请对重要文件进行备份处理，防止文件丢失


"""
        
        license_text = scrolledtext.ScrolledText(
            frame,
            wrap='word',
            font=('Microsoft YaHei UI', 10),
            padx=20,
            pady=20
        )
        license_text.insert('1.0', about2_text)
        license_text.config(state='disabled')  # 设置为只读
        license_text.pack(fill='both', expand=True)



    def setup_LICENSE_tab(self):
        frame = self.LICENSE_frame
        about_text = """
GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991

 Copyright (C) 1989, 1991 Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The licenses for most software are designed to take away your
freedom to share and change it.  By contrast, the GNU General Public
License is intended to guarantee your freedom to share and change free
software--to make sure the software is free for all its users.  This
General Public License applies to most of the Free Software
Foundation's software and to any other program whose authors commit to
using it.  (Some other Free Software Foundation software is covered by
the GNU Lesser General Public License instead.)  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
this service if you wish), that you receive source code or can get it
if you want it, that you can change the software or use pieces of it
in new free programs; and that you know you can do these things.

  To protect your rights, we need to make restrictions that forbid
anyone to deny you these rights or to ask you to surrender the rights.
These restrictions translate to certain responsibilities for you if you
distribute copies of the software, or if you modify it.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must give the recipients all the rights that
you have.  You must make sure that they, too, receive or can get the
source code.  And you must show them these terms so they know their
rights.

  We protect your rights with two steps: (1) copyright the software, and
(2) offer you this license which gives you legal permission to copy,
distribute and/or modify the software.

  Also, for each author's protection and ours, we want to make certain
that everyone understands that there is no warranty for this free
software.  If the software is modified by someone else and passed on, we
want its recipients to know that what they have is not the original, so
that any problems introduced by others will not reflect on the original
authors' reputations.

  Finally, any free program is threatened constantly by software
patents.  We wish to avoid the danger that redistributors of a free
program will individually obtain patent licenses, in effect making the
program proprietary.  To prevent this, we have made it clear that any
patent must be licensed for everyone's free use or not licensed at all.

  The precise terms and conditions for copying, distribution and
modification follow.

                    GNU GENERAL PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. This License applies to any program or other work which contains
a notice placed by the copyright holder saying it may be distributed
under the terms of this General Public License.  The "Program", below,
refers to any such program or work, and a "work based on the Program"
means either the Program or any derivative work under copyright law:
that is to say, a work containing the Program or a portion of it,
either verbatim or with modifications and/or translated into another
language.  (Hereinafter, translation is included without limitation in
the term "modification".)  Each licensee is addressed as "you".

Activities other than copying, distribution and modification are not
covered by this License; they are outside its scope.  The act of
running the Program is not restricted, and the output from the Program
is covered only if its contents constitute a work based on the
Program (independent of having been made by running the Program).
Whether that is true depends on what the Program does.

  1. You may copy and distribute verbatim copies of the Program's
source code as you receive it, in any medium, provided that you
conspicuously and appropriately publish on each copy an appropriate
copyright notice and disclaimer of warranty; keep intact all the
notices that refer to this License and to the absence of any warranty;
and give any other recipients of the Program a copy of this License
along with the Program.

You may charge a fee for the physical act of transferring a copy, and
you may at your option offer warranty protection in exchange for a fee.

  2. You may modify your copy or copies of the Program or any portion
of it, thus forming a work based on the Program, and copy and
distribute such modifications or work under the terms of Section 1
above, provided that you also meet all of these conditions:

    a) You must cause the modified files to carry prominent notices
    stating that you changed the files and the date of any change.

    b) You must cause any work that you distribute or publish, that in
    whole or in part contains or is derived from the Program or any
    part thereof, to be licensed as a whole at no charge to all third
    parties under the terms of this License.

    c) If the modified program normally reads commands interactively
    when run, you must cause it, when started running for such
    interactive use in the most ordinary way, to print or display an
    announcement including an appropriate copyright notice and a
    notice that there is no warranty (or else, saying that you provide
    a warranty) and that users may redistribute the program under
    these conditions, and telling the user how to view a copy of this
    License.  (Exception: if the Program itself is interactive but
    does not normally print such an announcement, your work based on
    the Program is not required to print an announcement.)

These requirements apply to the modified work as a whole.  If
identifiable sections of that work are not derived from the Program,
and can be reasonably considered independent and separate works in
themselves, then this License, and its terms, do not apply to those
sections when you distribute them as separate works.  But when you
distribute the same sections as part of a whole which is a work based
on the Program, the distribution of the whole must be on the terms of
this License, whose permissions for other licensees extend to the
entire whole, and thus to each and every part regardless of who wrote it.

Thus, it is not the intent of this section to claim rights or contest
your rights to work written entirely by you; rather, the intent is to
exercise the right to control the distribution of derivative or
collective works based on the Program.

In addition, mere aggregation of another work not based on the Program
with the Program (or with a work based on the Program) on a volume of
a storage or distribution medium does not bring the other work under
the scope of this License.

  3. You may copy and distribute the Program (or a work based on it,
under Section 2) in object code or executable form under the terms of
Sections 1 and 2 above provided that you also do one of the following:

    a) Accompany it with the complete corresponding machine-readable
    source code, which must be distributed under the terms of Sections
    1 and 2 above on a medium customarily used for software interchange; or,

    b) Accompany it with a written offer, valid for at least three
    years, to give any third party, for a charge no more than your
    cost of physically performing source distribution, a complete
    machine-readable copy of the corresponding source code, to be
    distributed under the terms of Sections 1 and 2 above on a medium
    customarily used for software interchange; or,

    c) Accompany it with the information you received as to the offer
    to distribute corresponding source code.  (This alternative is
    allowed only for noncommercial distribution and only if you
    received the program in object code or executable form with such
    an offer, in accord with Subsection b above.)

The source code for a work means the preferred form of the work for
making modifications to it.  For an executable work, complete source
code means all the source code for all modules it contains, plus any
associated interface definition files, plus the scripts used to
control compilation and installation of the executable.  However, as a
special exception, the source code distributed need not include
anything that is normally distributed (in either source or binary
form) with the major components (compiler, kernel, and so on) of the
operating system on which the executable runs, unless that component
itself accompanies the executable.

If distribution of executable or object code is made by offering
access to copy from a designated place, then offering equivalent
access to copy the source code from the same place counts as
distribution of the source code, even though third parties are not
compelled to copy the source along with the object code.

  4. You may not copy, modify, sublicense, or distribute the Program
except as expressly provided under this License.  Any attempt
otherwise to copy, modify, sublicense or distribute the Program is
void, and will automatically terminate your rights under this License.
However, parties who have received copies, or rights, from you under
this License will not have their licenses terminated so long as such
parties remain in full compliance.

  5. You are not required to accept this License, since you have not
signed it.  However, nothing else grants you permission to modify or
distribute the Program or its derivative works.  These actions are
prohibited by law if you do not accept this License.  Therefore, by
modifying or distributing the Program (or any work based on the
Program), you indicate your acceptance of this License to do so, and
all its terms and conditions for copying, distributing or modifying
the Program or works based on it.

  6. Each time you redistribute the Program (or any work based on the
Program), the recipient automatically receives a license from the
original licensor to copy, distribute or modify the Program subject to
these terms and conditions.  You may not impose any further
restrictions on the recipients' exercise of the rights granted herein.
You are not responsible for enforcing compliance by third parties to
this License.

  7. If, as a consequence of a court judgment or allegation of patent
infringement or for any other reason (not limited to patent issues),
conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot
distribute so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you
may not distribute the Program at all.  For example, if a patent
license would not permit royalty-free redistribution of the Program by
all those who receive copies directly or indirectly through you, then
the only way you could satisfy both it and this License would be to
refrain entirely from distribution of the Program.

If any portion of this section is held invalid or unenforceable under
any particular circumstance, the balance of the section is intended to
apply and the section as a whole is intended to apply in other
circumstances.

It is not the purpose of this section to induce you to infringe any
patents or other property right claims or to contest validity of any
such claims; this section has the sole purpose of protecting the
integrity of the free software distribution system, which is
implemented by public license practices.  Many people have made
generous contributions to the wide range of software distributed
through that system in reliance on consistent application of that
system; it is up to the author/donor to decide if he or she is willing
to distribute software through any other system and a licensee cannot
impose that choice.

This section is intended to make thoroughly clear what is believed to
be a consequence of the rest of this License.

  8. If the distribution and/or use of the Program is restricted in
certain countries either by patents or by copyrighted interfaces, the
original copyright holder who places the Program under this License
may add an explicit geographical distribution limitation excluding
those countries, so that distribution is permitted only in or among
countries not thus excluded.  In such case, this License incorporates
the limitation as if written in the body of this License.

  9. The Free Software Foundation may publish revised and/or new versions
of the General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

Each version is given a distinguishing version number.  If the Program
specifies a version number of this License which applies to it and "any
later version", you have the option of following the terms and conditions
either of that version or of any later version published by the Free
Software Foundation.  If the Program does not specify a version number of
this License, you may choose any version ever published by the Free Software
Foundation.

  10. If you wish to incorporate parts of the Program into other free
programs whose distribution conditions are different, write to the author
to ask for permission.  For software which is copyrighted by the Free
Software Foundation, write to the Free Software Foundation; we sometimes
make exceptions for this.  Our decision will be guided by the two goals
of preserving the free status of all derivatives of our free software and
of promoting the sharing and reuse of software generally.

                            NO WARRANTY

  11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
REPAIR OR CORRECTION.

  12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED
TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY
YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER
PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGES.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
convey the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Also add information on how to contact you by electronic and paper mail.

If the program is interactive, make it output a short notice like this
when it starts in an interactive mode:

    Gnomovision version 69, Copyright (C) year name of author
    Gnomovision comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, the commands you use may
be called something other than `show w' and `show c'; they could even be
mouse-clicks or menu items--whatever suits your program.

You should also get your employer (if you work as a programmer) or your
school, if any, to sign a "copyright disclaimer" for the program, if
necessary.  Here is a sample; alter the names:

  Yoyodyne, Inc., hereby disclaims all copyright interest in the program
  `Gnomovision' (which makes passes at compilers) written by James Hacker.

  <signature of Ty Coon>, 1 April 1989
  Ty Coon, President of Vice

This General Public License does not permit incorporating your program into
proprietary programs.  If your program is a subroutine library, you may
consider it more useful to permit linking proprietary applications with the
library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.

"""
        
        # 使用 ScrolledText 显示 LICENSE 文本
        license_text = scrolledtext.ScrolledText(
            frame,
            wrap='word',
            font=('Microsoft YaHei UI', 10),
            padx=20,
            pady=20
        )
        license_text.insert('1.0', about_text)
        license_text.config(state='disabled')  # 设置为只读
        license_text.pack(fill='both', expand=True)

    def log_obf(self, msg):
        self.obf_log.insert('end', msg + '\n')
        self.obf_log.see('end')
        self.root.update_idletasks()

    def log_rst(self, msg):
        self.rst_log.insert('end', msg + '\n')
        self.rst_log.see('end')
        self.root.update_idletasks()

    def browse_obf_source(self):
        path = filedialog.askdirectory(title="选择源文件夹")
        if path:
            self.obf_source_var.set(path)
            self.config['last_source'] = path

    def save_obf_output(self):
        path = filedialog.asksaveasfilename(defaultextension='.zip', filetypes=[('ZIP 文件', '*.zip')])
        if path:
            self.obf_output_var.set(path)
            self.config['last_output'] = path

    def browse_rst_input(self):
        path = filedialog.askopenfilename(filetypes=[('ZIP 文件', '*.zip'), ('所有文件', '*.*')])
        if path:
            self.rst_input_var.set(path)

    def select_rst_output(self):
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.rst_output_var.set(path)

    def get_selected_extensions(self, preset_vars: dict, custom_var: tk.StringVar) -> List[str]:
        exts = [ext for ext, var in preset_vars.items() if var.get()]
        custom = custom_var.get().strip()
        if custom and not custom.startswith('.'):
            custom = '.' + custom
        if custom and custom not in exts:
            exts.append(custom)
        return exts

    def add_obf_custom(self):
        ext = self.obf_custom_var.get().strip()
        if ext:
            if not ext.startswith('.'):
                ext = '.' + ext
            if ext not in self.obf_preset_vars:
                var = tk.BooleanVar(value=True)
                self.obf_preset_vars[ext] = var
                if ext not in self.config['extensions']:
                    self.config['extensions'][ext] = {
                        'temp': ext + '1',
                        'fake_hex': generate_fake_hex(ext)
                    }
                    save_config(self.config)
                self.log_obf(f"✓ 添加自定义后缀：{ext}")
                self.obf_custom_var.set('')

    def add_rst_custom(self):
        ext = self.rst_custom_var.get().strip()
        if ext:
            if not ext.startswith('.'):
                ext = '.' + ext
            if ext not in self.rst_preset_vars:
                var = tk.BooleanVar(value=True)
                self.rst_preset_vars[ext] = var
                if ext not in self.config['extensions']:
                    self.config['extensions'][ext] = {
                        'temp': ext + '1',
                        'fake_hex': generate_fake_hex(ext)
                    }
                    save_config(self.config)
                self.log_rst(f"✓ 添加自定义后缀：{ext}")
                self.rst_custom_var.set('')

    def select_all_obf(self):
        for var in self.obf_preset_vars.values():
            var.set(True)

    def clear_all_obf(self):
        for var in self.obf_preset_vars.values():
            var.set(False)

    def select_all_rst(self):
        for var in self.rst_preset_vars.values():
            var.set(True)

    def clear_all_rst(self):
        for var in self.rst_preset_vars.values():
            var.set(False)

    def load_last_config(self):
        if self.config.get('last_source'):
            self.obf_source_var.set(self.config['last_source'])
        if self.config.get('last_output'):
            self.obf_output_var.set(self.config['last_output'])
            self.rst_output_var.set(self.config['last_output'])

    def start_obfuscate(self):
        source = self.obf_source_var.get()
        output = self.obf_output_var.get()
        if not source or not output:
            messagebox.showwarning("参数缺失", "请填写源文件夹和输出 ZIP 路径")
            return
        
        selected_exts = self.get_selected_extensions(self.obf_preset_vars, self.obf_custom_var)
        if not selected_exts:
            if not messagebox.askyesno("确认", "未选择任何后缀，将混淆所有支持的文件？\n点击【是】继续，【否】取消"):
                return
            selected_exts = list(DEFAULT_EXTENSIONS.keys())
        
        self.obf_log.delete('1.0', 'end')
        self.obf_progress['value'] = 0
        self.status_var.set("正在混淆...")
        
        def run():
            try:
                obf = Obfuscator(self.config, selected_exts, self.log_obf)
                obf.create(source, output, self.obf_compress_var.get(),
                          lambda p: self.root.after(0, lambda: self.obf_progress.config(value=p)))
                self.root.after(0, lambda: [
                    self.status_var.set("✓ 混淆完成"),
                    messagebox.showinfo("成功", f"混淆完成!\n输出：{output}\n哈希：{calculate_file_hash(output)}")
                ])
                self.config.update({'last_source': source, 'last_output': output, 
                                   'compress': self.obf_compress_var.get()})
                save_config(self.config)
            except Exception as e:
                import traceback
                self.root.after(0, lambda: [
                    self.status_var.set("✗ 混淆失败"),
                    messagebox.showerror("错误", f"混淆失败:\n{e}")
                ])
                self.log_obf(f"❌ 错误：{e}")
                self.log_obf(traceback.format_exc())
        
        threading.Thread(target=run, daemon=True).start()

    def start_restore(self):
        zip_file = self.rst_input_var.get()
        output_dir = self.rst_output_var.get()
        if not zip_file or not output_dir:
            messagebox.showwarning("参数缺失", "请填写输入 ZIP 和输出目录")
            return
        
        selected_exts = self.get_selected_extensions(self.rst_preset_vars, self.rst_custom_var)
        if not selected_exts:
            if not messagebox.askyesno("确认", "未选择任何后缀，将恢复所有支持的扩展名？\n点击【是】继续，【否】取消"):
                return
            selected_exts = list(DEFAULT_EXTENSIONS.keys())
        
        self.rst_log.delete('1.0', 'end')
        self.rst_progress['value'] = 0
        self.status_var.set("正在恢复...")
        
        def run():
            try:
                rst = Restorer(self.config, selected_exts, self.log_rst)
                rst.restore(zip_file, output_dir, False,
                           lambda p: self.root.after(0, lambda: self.rst_progress.config(value=p)))
                self.root.after(0, lambda: [
                    self.status_var.set("✓ 恢复完成"),
                    messagebox.showinfo("成功", f"恢复完成!\n输出目录：{output_dir}")
                ])
            except Exception as e:
                import traceback
                self.root.after(0, lambda: [
                    self.status_var.set("✗ 恢复失败"),
                    messagebox.showerror("错误", f"恢复失败:\n{e}")
                ])
                self.log_rst(f"❌ 错误：{e}")
                self.log_rst(traceback.format_exc())
        
        threading.Thread(target=run, daemon=True).start()
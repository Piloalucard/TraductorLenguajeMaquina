
                    CodeView Update Patch Instructions

     (C) Copyright 1993 Microsoft Corporation.  All rights reserved.

     This document contains instructions for installing and using this
     CodeView update patch.  The information in this document is more
     up-to-date than that in the Microsoft Macro Assembler manuals.

     The version of CodeView (4.01) that shipped with MASM 6.11
     prohibited users from debugging and viewing source code in .COM
     files and from single-stepping through code that included 32-bit
     registers or floating point registers.  This update of CodeView
     (4.10) corrects those bugs.

     Because some of the command-line utilities work in concert with
     CodeView, they are included with this patch and must be copied
     to your hard disk with the CodeView files.
                                          

=============================< CONTENTS >=============================

     This file has the following sections:

     Part 1: Installation Instructions

     Part 2: What Has Been Fixed

     Part 3: Utilities Update

     Part 4: CodeView Update Bugs



=====================< INSTALLATION INSTRUCTIONS >====================


     1. Make backup copies of the files affected by the patch.  These 
        files should be in the MASM Bin directory (for example, 
        C:\MASM611\BIN).  Copy the following files:

        CV.EXE
        CVW.EXE
        CVW4.EXE
        BSCMAKE.EXE
        CVPACK.EXE
        EXEHDR.EXE
        IMPLIB.EXE
        LIB.EXE
        LINK.EXE
        SBRPACK.EXE
        CVW1.386
        EED1CXX.DLL
        EEW0CXX.DLL
        EMD1D1.DLL
        EMW0W0.DLL
        SHD1.DLL
        SHW0.DLL
        TLD1LOC.DLL
        TLW0LOC.DLL

     2. Copy the files from each distribution disk into your MASM Bin
        directory. For example, if you were installing from your A: 
        drive and your MASM Bin directory was C:\MASM611\BIN you would 
        enter:

        COPY A:\*.* C:\MASM611\BIN



========================< WHAT HAS BEEN FIXED >=========================


      This patch includes an updated version of CodeView (version 4.10).
      This new version enables you to perform the following three
      operations that were prohibited in CodeView 4.01:

      * You can single-step through code that uses 32-bit registers even
        while a DPMI server (such as Windows 3.1 or 386-MAX) is present.

      * Floating point registers can be viewed.

      * You can debug and view source code in .COM files.



=========================< UTILITIES UPDATE >=========================


     Basic Information
     -----------------
     The utilities included with this patch and their version numbers
     are listed below.  Several of these utilities are now 32-bit
     MS-DOS-extended programs, as marked.

          Filename                  Version
          --------                  -------
          BSCMAKE.EXE (32-bit)      2.50
          CVPACK.EXE (32-bit)       4.10
          EXEHDR.EXE                3.10
          IMPLIB.EXE                1.41
          LIB.EXE                   3.31
          LINK.EXE (32-bit)         5.50
          SBRPACK.EXE               2.10

     The 32-bit MS-DOS-extended utilities require an 80386 or higher
     processor running in protected mode.  The file DOSXNT.EXE must
     be in the same directory as the utility or in a directory
     specified in the PATH environment variable.  In addition, for
     these utilities to run with the Microsoft Windows operating
     system, DOSXNT.386 must be specified in a DEVICE statement
     in the [386Enh] section of the SYSTEM.INI file.

     QuickHelp is not available with the new version of these
     utilities.  The /HELP option for each utility now behaves the
     same as the /? option.  Both options display a brief summary of
     syntax and options for the tool.


     BSCMAKEV.EXE Obsolete
     ---------------------
     The utility BSCMAKEV.EXE that was included in MASM 6.11
     is now obsolete because of the upgrade to BSCMAKE.EXE.  You can
     delete BSCMAKEV.EXE from your disk and path.  Be sure to modify
     makefiles and batch files that contain this command.


     LINK.EXE Changes
     ----------------
     Make the following changes in "Environment and Tools":

          Page 457, Linking Object Files with LINK
          ----------------------------------------
          Strike out the third paragraph.  LINK no longer looks for
          CVPACK when linking a program for debugging.  LINK now
          provides the functionality of CVPACK.

          Page 458, New Features
          ----------------------
          The /r option has been removed.


          Page 476, The /EXEPACK Option
          -----------------------------
          Strike out the last sentence of the second paragraph.  In the
          third paragraph, add "and programs for Windows" to the
          end of the last sentence.


          Pages 494, Syntax Rules
          -----------------------
          Replace the first sentence in the last syntax rule with
          the following:

          If a string argument matches a reserved word or begins with
          a character other than a letter of the alphabet or an
          underscore (_), it must be enclosed in double quotation
          marks (" ").



=====================< CODEVIEW UPDATE BUGS  >=========================

     A few bugs have been found to occur when you use CodeView 4.10
     with MASM 6.11.  The known bugs and their workarounds are listed
     below.


     Spawning Problem
     ----------------
     If you are not using Microsoft Windows, a fatal error can result
     if an MS-DOS-extended utility spawns a real-mode utility,
     which then spawns an MS-DOS-extended utility.  The real-mode
     utilities which could potentially spawn a 32-bit utility are
     CREF and PWBRMAKE (both of which can spawn BSCMAKE).

     To avoid this problem, do one of the following:
        * Replace PWBRMAKE with BSCMAKE in makefiles.  Instead of
          running CREF on .SBR files, use BSCMAKE to convert the .SBR
          files into a .BSC file and then run CREF on the .BSC file.
        * Run from an MS-DOS prompt inside Windows.
        * Use NMAKER rather than NMAKE to control builds.


     Variable in Sample Programs Causes Reboot
     -----------------------------------------
     In the WINDLL samples, a tagWNDCLASS structure is occasionally
     used as a local variable.  If you expand this variable or others
     of this type in the Watch window or Locals window in CodeView
     version 4.10, the program may cause your computer to reboot.


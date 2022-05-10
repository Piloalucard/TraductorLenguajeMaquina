        .XLIST
;;  PCMac.inc--Macro INCLUDE file to be used with "Assembly Language
;;   for the IBM PC Family" by William B. Jones, (c) Copyright 1992,
;;   1997, 2001, Scott/Jones, Inc.

;;  This file has two versions of all the DOS call macros--one beginning '_'
;;   which does not save or restore any registers, and one beginning 's'
;;   that saves and restores all of the registers ax, bx, cx, and dx which
;;   are used by the macro and not used to return a value.

_Begin  MACRO
        mov     ax, @data
        mov     ds, ax
        mov     bx, ss
        sub     bx, ax
        shl     bx, 4
        mov     ss, ax
        add     sp, bx
        ENDM

; The following code is necessary to get the .TYPE function to work properly
; in TASM 5. ??VERSION is a built-in variable defined ONLY in TASM

IFDEF ??VERSION
    IF ??VERSION GE 500h
        OPTION  DOTNAME
    ENDIF
ENDIF

_LdAddr MACRO   reg, addr
IF (.TYPE (addr)) AND 10000B    ;; Register
        mov     reg, addr
ELSE
    IF (.TYPE (addr)) AND 100B  ;; Constant
        mov     reg, addr
    ELSE
        IF TYPE (addr) EQ 1             ;; Bytes
        lea     reg, addr
        ELSE
            IF TYPE (addr) EQ 2         ;; Near pointer
        mov     reg, addr
            ELSE
                IF TYPE (addr) EQ 4             ;; Far pointer
        lds     reg, addr
                ELSE
        .ERR
        %OUT    Illegal argument
                ENDIF
            ENDIF
        ENDIF
    ENDIF
ENDIF
ENDM

_LdSeg  MACRO   reg, segm
IFNB <segm>
    IFIDNI <segm>, <es>         ;; Segment register
        mov     ax, segm
        mov     reg, ax
    ELSE
        IFIDNI  <segm>, <ds>
        mov     ax, segm
        mov     reg, ax
        ELSE
            IFIDNI      <segm>, <cs>
        mov     ax, segm
        mov     reg, ax
            ELSE
                IFIDNI  <segm>, <ss>
        mov     ax, segm
        mov     reg, ax
                ELSE
        mov     ax, segm
        mov     reg, ax
                ENDIF
            ENDIF
        ENDIF
    ENDIF
ENDIF
ENDM

_SvRegs MACRO   reglist
        IRP     x, <reglist>
        push    x
        ENDM
        ENDM

_RsRegs MACRO   reglist
        IRP     x, <reglist>
        pop     x
        ENDM
        ENDM

_PutStr MACRO   addr, segm
        _LdAddr dx, <addr>
        _LdSeg  ds, <segm> ;; load segment second in case ax used in addr
        mov     ah, 09h
        int     21h
        ENDM

sPutStr MACRO   addr, segm
        _SvRegs <ax, dx>
        _PutStr <addr>, <segm>
        _RsRegs <dx, ax>
        ENDM

_PutCh  MACRO   c1, c2, c3, c4, c5, c6, c7, c8, c9, c10
        mov     ah, 02h
IFB <c1>
        int     21h ;;  char already in dl
ELSE
        IRP     x, <c1, c2, c3, c4, c5, c6, c7, c8, c9, c10>
    IFB <x>
        EXITM
    ENDIF
        mov     dl, x
        int     21h
        ENDM
ENDIF
        ENDM

sPutCh  MACRO   c1, c2, c3, c4, c5, c6, c7, c8, c9, c10
        _SvRegs <ax, dx>
        _PutCh  c1, c2, c3, c4, c5, c6, c7, c8, c9, c10
        _RsRegs <dx, ax>
        ENDM

_GetCh  MACRO   echo
IFIDNI  <&echo&>, <noEcho>
        mov     ah, 08h
ELSE
    IFIDNI <&echo&>, <0>
        mov     al, 08h
    ELSE
        mov     ah, 01h
    ENDIF
ENDIF
        int     21h
        ENDM

sGetCh  MACRO   echo
        _GetCh  echo
        ENDM    

_BIOSCh MACRO
        mov     ah, 0h
        int     16h
        ENDM

sBIOSCh MACRO
        _BIOSCh
        ENDM

_GetStr MACRO   Structure, segm
        _LdAddr dx, <Structure>
        _Ldseg  ds, <segm>
        mov     ah, 0Ah
        int     21h
        ENDM

sGetStr MACRO   Structure, segm
        _SvRegs <ax, dx>
        _GetStr <Structure>, <segm>
        _RsRegs <dx, ax>
        ENDM

_GetDate MACRO
        mov     ah, 2ah
        int     21h
        ENDM

sGetDate MACRO
        _GetDate
        ENDM

_GetTime MACRO
        mov     ah, 2ch
        int     21h
        ENDM

sGetTime MACRO
        _GetTime
        ENDM

_Open   MACRO   filename, accesstype, segm
        _LdAddr dx, <filename>
        _LdSeg  ds, <segm>
        mov     ah, 3dh
IFB     <&accesstype&>
        mov     al, 0
ELSE
    IFIDNI <&accesstype&>, <Read>
        mov     al, 0
    ELSE
        IFIDNI <&accesstype&>, <Write>
        mov     al, 1
        ELSE
            IFIDNI <&accesstype&>, <ReadWrite>
        mov     al, 2
            ELSE
        mov     al, accesstype
            ENDIF
        ENDIF
    ENDIF
ENDIF
        int     21h
        ENDM

sOpen   MACRO   filename, accesstype, segm
        _SvRegs <dx>
        _Open   <filename>, <accesstype>, <segm>
        _RsRegs <dx>
        ENDM

_Creat  MACRO   filename, segm
        sub     cx, cx
        _LdAddr dx, <filename>
        _LdSeg  ds, <segm>
        mov     ah, 3ch
        int     21h
        ENDM

sCreat  MACRO   filename, segm
        _SvRegs <dx>
        _Creat  <filename>, <segm>
        _RsRegs <dx>
        ENDM

_Close  MACRO   handle
        mov     bx, handle
        mov     ah, 3eh
        int     21h
        ENDM

sClose  MACRO   handle
        _SvRegs <bx>
        _Close  <handle>
        _RsRegs <bx>
        ENDM

_Read   MACRO   handle, offs, count, segm
        mov     cx, count
        mov     bx, handle
        _LdAddr dx, <offs>
        _LdSeg  ds, <segm>
        mov     ah, 3fh
        int     21h
        ENDM

sRead   MACRO   handle, offs, count, segm
        _SvRegs <bx, cx, dx>
        _Read   <handle>, <offs>, <count>, <segm>
        _RsRegs <dx, cx, bx>
        ENDM

_Write  MACRO   handle, offs, count, segm
        mov     cx, count
        mov     bx, handle
        _LdAddr dx, <offs>
        _LdSeg  ds, <segm>
        mov     ah, 40h
        int     21h
        ENDM

sWrite  MACRO   handle, offs, count, segm
        _SvRegs <bx, cx, dx>
        _Write  <handle>, <offs>, <count>, <segm>
        _RsRegs <dx, cx, bx>
        ENDM

_LSeek  MACRO   Handle, SeekType, LoDistance, HiDistance
IFNB <HiDistance>
        mov     cx, HiDistance
        mov     dx, LoDistance
ELSE
    IFDIFI <LoDistance>, <ax>
        mov     ax, LoDistance
    ENDIF
        cwd
        mov     cx, dx
        mov     dx, ax
ENDIF
        mov     bx, Handle
        mov     ah, 42h
IFIDNI <SeekType>, <FromStart>
        mov     al, 0
ELSE
    IFIDNI <SeekType>, <FromCur>
        mov     al, 1
    ELSE
        IFIDNI <SeekType>, <FromEnd>
        mov     al, 2
        ELSE
        mov     al, SeekType
        ENDIF
    ENDIF
ENDIF
        int     21h
        ENDM

sLSeek  MACRO   Handle, SeekType, LoDistance, HiDistance
        _SvRegs <bx, cx>
        _LSeek  <Handle>, <SeekType>, <LoDistance>, <HiDistance>
        _RsRegs <cx, bx>
        ENDM

_Exit   MACRO   ReturnVal
IFNB    <ReturnVal>
        mov     al, ReturnVal
ENDIF
        mov     ah, 4ch
        int     21h
        ENDM

sExit   MACRO   ReturnVal
        _Exit   <ReturnVal>
        ENDM

_SetIntVec MACRO intr, Handler
        push    ds
IF TYPE(Handler) EQ 4
        lds     dx, Handler ; Handler is DWORD PTR to routine
ELSE
    IF TYPE(Handler) EQ 0FFFEh ;  FAR label
        mov     ax, SEG Handler
    ELSE
        mov     ax, cs
    ENDIF
        mov     ds, ax
        mov     dx, OFFSET Handler
ENDIF
        mov     ah, 25h
        mov     al, intr
        int     21h
        pop     ds
        ENDM

sSetIntVec MACRO intr, Handler
        _SvRegs <dx>
        _SetIntVec      <intr>, <Handler>
        _RsRegs <dx>
        ENDM

_SaveIntVec MACRO intr, OldIntVec
        mov     ah, 35h
        mov     al, intr
        int     21h
        ASSUME  es:NOTHING
        mov     WORD PTR OldIntVec, bx
        mov     WORD PTR OldIntVec+2, es
        ENDM

sSaveIntVec MACRO intr, OldIntVec
        _SvRegs <bx>
        _SaveIntVec     <intr>, <OldIntVec>
        _RsRegs <bx>
        ENDM

??? MACRO   n ; Placeholder for debugging
    mov al, al
    ENDM

        .LIST

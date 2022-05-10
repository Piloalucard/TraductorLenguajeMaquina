;; FIRST.ASM--Our first Assembly Language Program.  This program 
;;   displays the line 'Hello, my name is Bill Jones' on the CRT screen.
;;
;;  Program text from "Assembly Language for the IBM PC Family" by
;;   William B. Jones, (c) Copyright 1992, 1997, 2001, Scott/Jones Inc.
;;
        .MODEL  SMALL
        .586

        .STACK  100h

        .DATA
Message DB  'Hello, my name is Bill Jones', 13, 10, '$'

        .CODE
Hello   PROC
        mov ax, @data
        mov ds, ax
        mov dx, OFFSET Message
        mov ah, 9h ;    The function code for 'display string'
        int 21h ;   The standard way to call MS/PCDOS
        mov al, 0 ; Return code of 0
        mov ah, 4ch ;   Exit back to MS/PCDOS
        int 21h
Hello   ENDP

        END Hello ; Tells where to start execution

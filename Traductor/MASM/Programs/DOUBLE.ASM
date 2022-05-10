;  DOUBLE  This program prompts the user to enter a number < 5,
;  doubles the number, and outputs the result
	name    double
	.model 	small
	.stack  100
	.data
prompt  db      0ah,0dh,"Enter a number < 5: $"
resmes  db	0ah,0dh,"Double your number is: "
result  db  ?,0ah,0dh,"$"
	.code 
start:	
 	mov	ax, @data
	mov	ds, ax
        lea     dx, prompt
	mov	ah, 9		;dos fn to output string up to $
	int	21h
	mov	ah, 1		;dos fn to input byte into al
 	int	21h
	sub	al, 30h		;convert from ascii to integer
	add	al, al
	add al, 30h     ;convert back to ascii 
   	mov	result, al
	lea	dx, resmes
	mov	ah, 9
	int 	21h
	mov	ax, 4c00h	;4c in ah is dos exit fn with return code in al
	int 	21h
	end	start

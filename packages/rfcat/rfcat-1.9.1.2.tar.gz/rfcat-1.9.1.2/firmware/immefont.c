#include "immeterm.h"


static const u8 font[fontSIZE]={
  //0x20 is a space, handy
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, //space
  0x00, 0x5f, 0x5f, 0x00, 0x00, 0x00, //!
  0x00, 0x03, 0x00, 0x03, 0x00, 0x00, //"
  0x14, 0x7f, 0x14, 0x7f, 0x14, 0x00, //#
  0,0,0,0,0,0,
  0x23, 0x13, 0x08, 0x64, 0x62, 0x00, //%
  0x00, 0x00, 0x07, 0x00, 0x00, 0x00, //'
  0,0,0,0,0,0,
  //28
  0,0,0,0,0,0,
  0,0,0,0,0,0,
  0,0,0,0,0,0,
  0,0,0,0,0,0,
  0,0,0,0,0,0,
  0,0,0,0,0,0,
  0,0,0,0,0,0,
  0,0,0,0,0,0,
  
  //0x30 in ASCII
  //0
  0x3e, 0x51, 0x49, 0x45, 0x3e, 0x00, //0
  0x00, 0x42, 0x7F, 0x40, 0x00, 0x00, //1
  0x42, 0x61, 0x51, 0x49, 0x46, 0x00, //2
  0x21, 0x41, 0x45, 0x4b, 0x31, 0x00, //3
  0x18, 0x14, 0x12, 0x7f, 0x10, 0x00, //4
  0x27, 0x45, 0x45, 0x45, 0x39, 0x00, //5
  0x3c, 0x4a, 0x49, 0x49, 0x30, 0x00, //6
  0x01, 0x71, 0x09, 0x05, 0x03, 0x00, //7
  0x36, 0x49, 0x49, 0x49, 0x36, 0x00, //8
  0x06, 0x49, 0x49, 0x29, 0x1e, 0x00, //9
  0x00, 0x36, 0x36, 0x00, 0x00, 0x00, //:
  0x00, 0x56, 0x36, 0x00, 0x00, 0x00, //;
  0x08, 0x14, 0x22, 0x41, 0x00, 0x00, //<
  0x14, 0x14, 0x14, 0x14, 0x14, 0x00, //=
  0x41, 0x22, 0x14, 0x08, 0x00, 0x00, //>
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x3e, 0x41, 0x5d, 0x49, 0x4f, 0x00, //@
  
  //Uppercase letters begin at 0x41
  0x7e, 0x09, 0x09, 0x09, 0x7e, 0x00, //A
  0x7f, 0x49, 0x49, 0x49, 0x36, 0x00, //B
  0x3e, 0x41, 0x41, 0x41, 0x22, 0x00, //C
  0x7f, 0x41, 0x41, 0x41, 0x3e, 0x00, //D
  0x7f, 0x49, 0x49, 0x49, 0x41, 0x00, //E
  0x7f, 0x09, 0x09, 0x09, 0x01, 0x00, //F
  0x3e, 0x41, 0x49, 0x49, 0x79, 0x00, //G
  0x7f, 0x08, 0x08, 0x08, 0x7f, 0x00, //H
  0x00, 0x41, 0x7f, 0x41, 0x00, 0x00, //I
  0x30, 0x40, 0x40, 0x40, 0x3f, 0x00, //J
  0x7f, 0x08, 0x14, 0x22, 0x41, 0x00, //K
  0x7f, 0x40, 0x40, 0x40, 0x40, 0x00, //L
  0x7f, 0x02, 0x0c, 0x02, 0x7f, 0x00, //M
  0x7f, 0x04, 0x08, 0x10, 0x7f, 0x00, //N
  0x3e, 0x41, 0x41, 0x41, 0x3e, 0x00, //O
  0x7f, 0x09, 0x09, 0x09, 0x06, 0x00, //P
  0x3c, 0x42, 0x52, 0x3c, 0x40, 0x00, //Q
  0x7f, 0x09, 0x19, 0x29, 0x46, 0x00, //R
  0x46, 0x49, 0x49, 0x49, 0x31, 0x00, //S
  0x01, 0x01, 0x7f, 0x01, 0x01, 0x00, //T
  0x7f, 0x40, 0x40, 0x40, 0x7f, 0x00, //U
  0x07, 0x18, 0x60, 0x18, 0x07, 0x00, //V
  0x3f, 0x40, 0x38, 0x40, 0x3f, 0x00, //W
  0x63, 0x1c, 0x08, 0x1c, 0x63, 0x00, //X
  0x03, 0x04, 0x7c, 0x04, 0x03, 0x00, //Y
  0x61, 0x61, 0x51, 0x49, 0x47, 0x00, //Z FIXME
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //\ 
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //]
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //^
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //_
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //`
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //a
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //b
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //c
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //d
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //e
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //f
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //g
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //h
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //i
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //j
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //k
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //l
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //m
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //n
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //o
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //p
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //q
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //r
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //s
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //t
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //u
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //v
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //w
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //x
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //y
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //z
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //{
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //|
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //}
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //~
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  0x02, 0x01, 0x51, 0x09, 0x06, 0x00, //?
  
  
  0
};



void putch(char ch){
  u16 start;
  u8 i;
  
  if(!ch){
    for(i=0;i<7;i++)
      txData(0x00);  
    return;
  }
  
  //uppercase
  if(ch>='a' && ch<='z')
    ch-=('a'-'A');

  start=ch-ASCIIOFFSET;
  start*=6;
  for(i=0;i<6;i++)
    txData(font[start+i]);
}

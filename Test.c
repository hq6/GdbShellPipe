#include <stdio.h>


int foo() {
    const char* buf = "Hello World \x1c";
    puts(buf);
}
int main(){
    foo();
}


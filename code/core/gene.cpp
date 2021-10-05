#include <iostream>
#include <fstream>
#include <iomanip>
using namespace std;


// void addi(int imm,int rs1,int rd);

void addi(std::ofstream & fs,int imm,int rs1,int rd) {
    fs <<  setbase(2) << setw(12) << 


}



int main() {
    using namespace std;
    ofstream fs;
    fs.open("instr.txt");
}
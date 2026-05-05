const editor = document.querySelector("#editor");
const output = document.querySelector("#console");
const taskDropDown = document.querySelector("#taskDD");
const compileBtn = document.querySelector("#compileBtn");
const resetBtn = document.querySelector("#resetBtn");
const clearBtn = document.querySelector("#clearBtn");
const tasks = new Object();

document.addEventListener("DOMContentLoaded", defineTasks());
taskDropDown.addEventListener("change", () => {setCode();});
clearBtn.addEventListener("click", () => {editor.value = ""; output.value="";});
resetBtn.addEventListener("click", () =>{setCode(); output.value="";});

editor.addEventListener("keydown", (e) => {
    if (e.keyCode === 9) {
        e.preventDefault();
        
        const cursorPos = editor.selectionStart;
        const currentValue = editor.value;
        
        // Insert 4 spaces directly
        editor.value = currentValue.substring(0, cursorPos) + "    " + currentValue.substring(editor.selectionEnd);
        editor.selectionStart = editor.selectionEnd = cursorPos + 4;
    }
});

compileBtn.addEventListener("click", async () =>{    

    const response = await fetch("api/compile", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({code : editor.value})
    });    

    const data = await response.json();
    console.log(data);


    if (data.returncode != 0){
        output.value = data.stderr;
    }else {
        output.value = data.stdout;
    }
});



function setCode(){
    editor.value = tasks[taskDropDown.value] ? tasks[taskDropDown.value] : "";
}


function defineTasks(){
tasks.print = `/*---------------------Task 1---------------------*/
/*Print a message to the console*/
/*-------------------------------------------------*/

integer main(){
    string s = "hello world";
    print(s);
    return 0;
}`;

tasks.count = 
`/*---------------------Task 2---------------------*/
/*Rewrite this code so it counts to 10 using a while loop*/
/*Bonus: make the program count down instead of up*/
/*-------------------------------------------------*/

integer main(){
    integer i = 0;
    while(i < 5){
        i = i + 1;
        print(i, ",");
    }
    return 0;
}`;

tasks.check =
`/*---------------------Task 3---------------------*/
/*Here is code that uses a function to get the sum of two numbers
Make functions that can subtract, multiply and devide (remember to do a 0 check) */
/*Bonus: Can it all be written in one function?*/
/*-------------------------------------------------*/

integer main(){
    double d = 5.5;
    integer a = 0;

    if(true){
        double result = d / a;
        print(result);
    } else{
        print("The denominator is 0 making it an illegal operation");
    }
    return 0;
}`; 

tasks.sum = 
`/*---------------------Task 4---------------------*/
/*Here is code that uses a function to get the sum of two numbers
Make functions that subtract multiply and devide
/*Bonus: Can it all be written in one function?*/
/*-------------------------------------------------*/

integer sum(integer a, integer b){
    return a + b;
}

integer main(){
    integer number = sum(1,2);

    print(number);
    return 0;
}`; 

tasks.square =
`/*---------------------Task 5---------------------*/
/*Here is a program that prints a square, can you make the square hollow*/
/* Bonus: can you make it draw a chess board instead*/
/*-------------------------------------------------*/

integer main(){
    integer i = 0;
    integer j = 0;

    while(i < 8){
        j = 0;
        while(j < 8){
            print("#");
            j = j + 1;
        }
        print("\\n");
        i = i + 1;
    }
    return 0;
}
`

tasks.array =
`/*---------------------Task 6---------------------*/
/*Here is an array can that prints index 0
can you print the whole array using a while loop?*/
/*Bonus: can you sort the array*/
/*-------------------------------------------------*/

integer main(){
    integer array[6] = [6,2,5,1,3,4];
    integer index = 0;
    
    print(array[index]);
    return 0;
}
`
}



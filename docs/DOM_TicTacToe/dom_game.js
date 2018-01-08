console.log("JavaScript is connnected!");
var restart = document.querySelector("#restart_game");
// Get all elements
restart.addEventListener("click", clearBoard);
var cells = document.getElementsByTagName('td');
console.log(cells);

function fillVals(){
  console.log('In fill vals');
  if(this.textContent === ''){
    this.textContent = 'X';
  }
  else if (this.textContent === 'X') {
    this.textContent = 'O';
  }
  else{
    this.textContent = '';
  }

}

for(var i=0; i<9;i++){
  cells[i].addEventListener("click",fillVals);
  //cells[i].addEventListener("dblclick", fillO(cells[i]));
}


function clearBoard(){
  for (var i = 0; i < cells.length; i++) {
    cells[i].textContent = ' ';
  }
}

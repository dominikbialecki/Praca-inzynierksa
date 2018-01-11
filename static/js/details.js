/*function button(id){
    var td = document.getElementById(id);
    if(td.style.display=='none'){
        td.style.display="table-row";
    }
    else{
        td.style.display="none";
    }
}
*/
function change(dane, i){
    var td = document.getElementById(i);
    if(td.style.display=='none'){
        td.style.display="table-row";
        document.getElementById(dane).classList.remove("glyphicon-plus");
        document.getElementById(dane).classList.add("glyphicon-minus");
    }
    else{
        td.style.display="none";
        document.getElementById(dane).classList.remove("glyphicon-minus");
        document.getElementById(dane).classList.add("glyphicon-plus");
    }
}

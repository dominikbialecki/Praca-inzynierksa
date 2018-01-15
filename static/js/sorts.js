function switching(id1,id2){
    var ids=['0','1','2','3'];
    var td = document.getElementById(id1);
    if(!td.classList.contains('active')){
        td.classList.add("active");
        document.getElementById(id2).classList.remove("active");
        for (i = 0; i < ids.length; i++) { 
            if(document.getElementById(ids[i]).classList.contains('active')){
                document.getElementById(ids[i]).classList.remove("active");
                if(document.getElementById(id2+ids[i]).style.display=='block'){
                        document.getElementById(id2+ids[i]).style.display='none';
                }
            }
        }
        document.getElementById("0").classList.add("active");
        document.getElementById(id1+"0").style.display='block';
    }
}

function change(check,id){
     var ids=['0','1','2','3'];
     for (i = 0; i < ids.length; i++) { 
            if(document.getElementById(ids[i]).classList.contains('active')){
                document.getElementById(ids[i]).classList.remove("active");
                if(document.getElementById(id+ids[i]).style.display=='block'){
                        document.getElementById(id+ids[i]).style.display='none';
                }
            }
        }
    document.getElementById(check).classList.add("active");
    document.getElementById(id+check).style.display='block';
}

function sortAlb(spanId){
    var box=document.getElementById('box');
    var list=document.getElementById('list');
    if(box.classList.contains('active') && document.getElementById('box'+spanId)!='block'){
        change(spanId,'box');
    }else if(list.classList.contains('active') && document.getElementById('box'+spanId)!='block'){
        change(spanId,'list');
    }
}

function blockAlb(id,id2){
    var td = document.getElementById(id);
    var ids=['0','1','2'];
    if(td.id=='blocks' && !td.classList.contains('active')){
        document.getElementById(id2).classList.remove("active");
        td.classList.add("active");
         /*document.getElementById('box').style.display='block'
        for (i = 0; i < ids.length; i++) { 
            if(document.getElementById(ids[i]).classList.contains('active')&& document.getElementById('list'+ids[i]).style.display=='block'){
               document.getElementById(ids[i]).classList.remove("active");
               document.getElementById('list'+ids[i]).style.display='none';
            }
        }*/
    }
}

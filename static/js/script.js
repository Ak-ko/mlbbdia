// START OF NAVBAR
// END OF NAVBAR

// START INPUT INVALIDS
var userid = document.querySelector('#userid');
var serverid = document.querySelector('#serverid');

userid.onblur = function(){
    let value = userid.value;
    if(!value){
        userid.classList.add('is-invalid');
        userid.style.border = '1px solid rgba(0,0,0,0.2)';
        userid.style.backgroundImage = 'none';
        userid.style.paddingLeft = '36px';
        userid.style.boxShadow = 'none';
    }
    else{
        userid.classList.remove('is-invalid');
        userid.style.paddingLeft = '0px';
    };
};

serverid.onblur = () => {
    let value = serverid.value;
    if(!value){
        serverid.classList.add('is-invalid');
        serverid.style.border = '1px solid rgba(0,0,0,0.2)';
        serverid.style.backgroundImage = 'none';
        serverid.style.paddingLeft = '36px';
        serverid.style.boxShadow = 'none';
    }
    else{
        serverid.classList.remove('is-invalid');
        serverid.style.paddingLeft = '0px';
    }
}
// END INPUT INVALIDS


// START SPAN QUESTION MARK
var errorimg = document.querySelector(".errorimgs");
var qusetionmark = document.querySelector(".questionmarks");

qusetionmark.onmouseover = function(){
    errorimg.style.display = 'block';
}
qusetionmark.onmouseout = function(){
    errorimg.style.display = 'none';
}
// END SPAN QUESTION MARK




// start footer section
const yearNow = document.querySelector('.yearNow');
const getYear = new Date().getFullYear();
yearNow.textContent = getYear;
// end footer section
console.log('connected');

function validateForm(){
        
    startdate = document.getElementById('startdate');
    endate = document.getElementById('endate');
    var sdate =new Date(startdate.value); 

    var smonth = sdate.getMonth(); // months start counting from zero!
    var sday   = sdate.getDate();  
    var syear  = sdate.getFullYear();

    alert(smonth)
    var d = new Date();
    var month = d.getMonth(); // months start counting from zero!
    var day   = d.getDate();  
    var year  = d.getFullYear();
    return false;
    }

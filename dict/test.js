var xmlHttpRequest;
function createXmlHttpRequest(){      
    if(window.ActiveXObject){ //如果是IE浏览器      
        return new ActiveXObject("Microsoft.XMLHTTP");      
    }else if(window.XMLHttpRequest){ //非IE浏览器      
        return new XMLHttpRequest();      
    }      
}
function getId(){      
    var url = "http://phiboxwechat.phicomm.com/wechat/user/myAccount?openId=7CEA534B9853597742FF3A60DFDAAA514BB0CD1EBBBF6610932A140134515B40";     
    xmlHttpRequest = createXmlHttpRequest();           
    xmlHttpRequest.onreadystatechange = zswFun;           
    xmlHttpRequest.open("GET",url,true);            
    xmlHttpRequest.send(null);        
}              
function zswFun(){      
    if(xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){      
        var b = xmlHttpRequest.responseText;      
        var txt = b.getElementById("myForm");
        alert(txt[0].value);            
    }      
}
getId();       

window.onload=function () {
    render();
  };
  function render() {
      window.recaptchaVerifier=new firebase.auth.RecaptchaVerifier('recaptcha-container');
      recaptchaVerifier.render();
  }
  function phoneAuth() {
      //get the number
      var number=document.getElementById('number').value;
      //phone number authentication function of firebase
      //it takes two parameter first one is number,,,second one is recaptcha
      firebase.auth().signInWithPhoneNumber(number,window.recaptchaVerifier).then(function (confirmationResult) {
          //s is in lowercase
          window.confirmationResult=confirmationResult;
          coderesult=confirmationResult;
          console.log(coderesult);
          document.getElementById('otp').style.display = "block";
          document.getElementById('SendCode').style.visibility = 'hidden';

          alert("Message sent");
      }).catch(function (error) {
          alert(error.message);
      });
  }
  function codeverify() {
      var code=document.getElementById('verificationCode').value;
      coderesult.confirm(code).then(function (result) {
          alert("Successfully registered");
          document.getElementById('otp').style.display = "none";
          document.getElementById("register").style.visibility = "visible";

          var user=result.user;
          console.log(user);
      }).catch(function (error) {
          alert(error.message);
      });
  }
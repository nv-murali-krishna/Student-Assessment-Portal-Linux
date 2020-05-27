function Logfunction()
{
    var empname = document.forms["RegForm"]["Name"];
    var empnumber =  document.forms["RegForm"]["Empnumber"];
    var email = document.forms["RegForm"]["Email"];
    var phone = document.forms["RegForm"]["Phone"];

  //  var Password = document.forms["RegForm"]["Password"];
    //var address = document.forms["RegForm"]["Address"];

    if (empname.id == "Name")
    {
        window.alert("Please enter your name.");
        name.focus();
        return false;
    }

    if (empnumber.id == "Empnumber")
    {
        window.alert("Please enter your number");
        address.focus();
        return false;
    }

    if (email.id == "Email")
    {
        window.alert("Please enter a valid email");
        email.focus();
        return false;
    }

    if (phone.id == "Phone")
    {
        window.alert("Please enter your phone number");
        phone.focus();
        return false;
    }

  /*  if (password.value == "")
    {
        window.alert("Please enter your password");
        password.focus();
        return false;
    }*/

  /*  if (what.selectedIndex < 1)
    {
        alert("Please enter your course.");
        what.focus();
        return false;
    }*/

    return true;
  }

  (function ($) {
      "use strict";

      /*==================================================================
      [ Focus Contact2 ]*/
      $('.input100').each(function(){
          $(this).on('blur', function(){
              if($(this).val().trim() != "") {
                  $(this).addClass('has-val');
              }
              else {
                  $(this).removeClass('has-val');
              }
          })
      })


      /*==================================================================
      [ Validate after type ]*/
      $('.validate-input .input100').each(function(){
          $(this).on('blur', function(){
              if(validate(this) == false){
                  showValidate(this);
              }
              else {
                  $(this).parent().addClass('true-validate');
              }
          })
      })

      /*==================================================================
      [ Validate ]*/
      var input = $('.validate-input .input100');

      $('.validate-form').on('submit',function(){
          var check = true;

          for(var i=0; i<input.length; i++) {
              if(validate(input[i]) == false){
                  showValidate(input[i]);
                  check=false;
              }
          }

          return check;
      });


      $('.validate-form .input100').each(function(){
          $(this).focus(function(){
             hideValidate(this);
             $(this).parent().removeClass('true-validate');
          });
      });

      function validate (input) {
          if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
              if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                  return false;
              }
          }
          else {
              if($(input).val().trim() == ''){
                  return false;
              }
          }
      }

      function showValidate(input) {
          var thisAlert = $(input).parent();

          $(thisAlert).addClass('alert-validate');
      }

      function hideValidate(input) {
          var thisAlert = $(input).parent();

          $(thisAlert).removeClass('alert-validate');
      }



  })(jQuery);

function gfunction()
{
    var first_name = document.forms["RegForm"]["first_name"];
    var email = document.forms["RegForm"]["EMail"];
    var last_name = document.forms["RegForm"]["last_name"];
    /*var what =  document.forms["RegForm"]["Subject"]; */
    var password = document.forms["RegForm"]["Password"];
    var re_password = document.forms["RegForm"]["re_password"];

    if (first_name.value == "")
    {
        window.alert("Please enter your name.");
        name.focus();
        return false;
    }

    if (last_name.value == "")
    {
        window.alert("Please enter your address.");
        address.focus();
        return false;
    }

    if (email.value == "")
    {
        window.alert("Please enter a valid e-mail address.");
        email.focus();
        return false;
    }

    if (re_password.value == "")
    {
        window.alert("Please enter your telephone number.");
        phone.focus();
        return false;
    }

    if (password.value == "")
    {
        window.alert("Please enter your password");
        password.focus();
        return false;
    }

  /*  if (what.selectedIndex < 1)
    {
        alert("Please enter your course.");
        what.focus();
        return false;
    } */

    return true;
}

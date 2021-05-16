window.onload = function() {
    console.log("this from child window" + window.opener.currentCountryName);
    document.getElementById('countryname').innerHTML = window.opener.currentCountryName;
}

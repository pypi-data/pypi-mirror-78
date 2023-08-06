// Defines the d3 library
require.config({
    paths: {
        "d3": "/custom/d3.min"
    }
});

// Loads myQLM/QLM scripts
require(
    ["custom/display_library", "custom/FileSaver"],
    function() { }
);

// Loads the d3 library
require(["d3"], function(d3) {
    window.d3 = d3;
    console.log("d3 loaded");
});

// Do not open a new tab for each Jupyter Notebook by default
// If a new tab is wanted, use ctrl^click ; like that, the user
// is in control
$('a').attr('target', '_self');
require(["base/js/namespace"], function (Jupyter) {
  Jupyter._target = '_self';
}); 


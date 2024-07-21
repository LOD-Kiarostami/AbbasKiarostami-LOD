/*!
 * Start Bootstrap - Scrolling Nav v5.0.5 (https://startbootstrap.com/template/scrolling-nav)
 * Copyright 2013-2022 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-scrolling-nav/blob/master/LICENSE)
 */
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function(responsiveNavItem) {
        responsiveNavItem.addEventListener('mouseenter', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});


// JAVASCRIPT FOR THE METADATA ALIGNMENT FILTERING



function filterSelection(groupName, c) {
    var x, i;
    x = document.getElementsByClassName('filterDiv ' + groupName);

    // Hide all elements with the specified groupName
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }

    // Show the elements that match the filter criteria
    for (i = 0; i < x.length; i++) {
        if (x[i].className.indexOf(c) > -1) {
            x[i].style.display = "block";
        }
    }
}

// Initial display setup
filterSelection("metaAlign", "who");
filterSelection("itemDesc", "treatise");

// Show filtered elements
function w3AddClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        if (arr1.indexOf(arr2[i]) == -1) {
            element.className += " " + arr2[i];
        }
    }
}

// Hide elements that are not selected
function w3RemoveClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        while (arr1.indexOf(arr2[i]) > -1) {
            arr1.splice(arr1.indexOf(arr2[i]), 1);
        }
    }
    element.className = arr1.join(" ");
}

// Add active class to the current control button (highlight it)
// JAVASCRIPT FOR THE METADATA ALIGNMENT FILTERING

function filterSelection(groupName, c, btn) {
    var i;
    var x = document.getElementsByClassName('filterDiv ' + groupName);

    // Hide all elements with the specified groupName
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }

    // Show the elements that match the filter criteria
    for (i = 0; i < x.length; i++) {
        if (x[i].className.indexOf(c) > -1) {
            x[i].style.display = "block";
        }
    }

    // Remove the "active" class from all buttons
    var btns = document.querySelectorAll('#myBtnContainer .btn');
    btns.forEach(function(btn) {
        btn.classList.remove('active');
    });

    // Add the "active" class to the clicked button
    btn.classList.add('active');
}

// Initial display setup
document.addEventListener('DOMContentLoaded', function() {
    var initialBtn = document.querySelector('#myBtnContainer .btn.active');
    if (initialBtn) {
        filterSelection('metaAlign', 'who', initialBtn);
    }
});







/*MODALS ZOOM IMAGE*/
var modals = document.getElementsByClassName('modalmyModal');
// Get the button that opens the modal
var btns = document.getElementsByClassName("openmodalmyBtn");
var spans = document.getElementsByClassName("close");
for (let i = 0; i < btns.length; i++) {
    btns[i].onclick = function() {
        modals[i].style.display = "block";
    }
}
for (let i = 0; i < spans.length; i++) {
    spans[i].onclick = function() {
        modals[i].style.display = "none";
    }
}
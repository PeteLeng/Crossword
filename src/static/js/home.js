// Create new HTML element
const display = document.getElementById("display");
let new_p = document.createElement('p');
new_p.id = 'newid';
let new_p_text = document.createTextNode('this is a new display');
new_p.appendChild(new_p_text);
display.appendChild(new_p);
// display.insertBefore(new_p,display.firstChild)


// Increment number when clicking button
let words = document.getElementById("id_words").value.split(",");
function next() {
    let tag = document.getElementById("idx");
    let idx = Number(tag.textContent) + 1;
    tag.textContent = idx;
    document.getElementById("active").textContent = words[idx % words.length]
}
document.getElementById("next").onclick = next;


let display_size = 10;
console.log(display_size);


// Define constant and variable
// Elements
const grid = document.getElementById("grid-container"); // Grid container
const transformed = document.getElementById(id="transformed"); // transformed location tag
const btn_grid = document.getElementById("grid");
const btn_plus = document.getElementById("plus");
const btn_minus = document.getElementById("minus");

// Source data
const locs = JSON.parse(document.getElementById("locations").innerHTML); // pattern location dictionaries
const cw_center = [2, 2];


// Event bindings
btn_plus.onclick = plus;
btn_minus.onclick = minus;
btn_grid.onclick = makeGrid;


// Functions
// Make grid
function makeGrid() {
    grid.style.setProperty('--grid-rows', display_size);
    grid.style.setProperty('--grid-cols', display_size);
    clearGrid();
    for (i = 0; i < display_size; i++) {
        for (j = 0; j < display_size; j++) {
            let cell = document.createElement('div');
            cell.id = '' + i + ',' + j;
            grid.appendChild(cell).className = 'grid-item';
        }
    }
    fillGrid();
}

// Clear grid
function clearGrid() {
    while (grid.firstChild) {
        grid.removeChild(grid.lastChild);
    }
}

// Fill grid
function fillGrid() {
    let display_locs = transform();
    for (var key in display_locs) {
        let cell = document.getElementById(key);
        cell.textContent = display_locs[key];
    }
}


// Increment display size
function plus() {
    display_size += 1;
    makeGrid();
}

// Decrement display size
function minus() {
    if (display_size > 5) {
        display_size -= 1;
        makeGrid();
    }
}

// Transformers
// Always put the crossword in the middle of the display
function transform() {
    let display_center = Math.floor(display_size / 2);
    let x_diff = display_center - cw_center[0];
    let y_diff = display_center - cw_center[1];
    let new_locs = {};
    for (var key in locs) {
        let loc = key.split(',').map(x => Number(x));
        let new_x = loc[0] + x_diff;
        let new_y = loc[1] + y_diff;
        new_locs['' + new_x + ',' + new_y] = locs[key];
    }
    // console.log(new_locs);
    return new_locs;
}
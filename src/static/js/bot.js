// Define constant and variable
// Elements
const btn_next = document.getElementById("next");
const btn_prev = document.getElementById("prev");
const btn_plus = document.getElementById("plus");
const btn_minus = document.getElementById("minus");
const btn_view = document.getElementById("preview");
const btn_save = document.getElementById("save");
const left = document.getElementById("left");
const grid = document.getElementById("grid-container");
const cross = document.getElementById("cross");
const down = document.getElementById("down");
const qs = document.getElementById(id="qs");
const qs_arr = JSON.parse(qs.innerHTML);

// Variables
let grid_size = 15;
let preview_mode = 0;
let idx = 0;
let crossword = qs_arr[idx];
let cw_locs = crossword.locations;
let cw_center = crossword.dimensions;
let cw_cross = crossword.cross;
let cw_down = crossword.down;
let cw_ordering = crossword.ordering;
let cw_words = Object.values(cw_cross).concat(Object.values(cw_down));
let display_locs = cw_locs;
let display_ordering = cw_ordering;
let hints = {};


// Event binding
btn_next.onclick = next;
btn_prev.onclick = prev;
btn_plus.onclick = plus;
btn_minus.onclick = minus;
btn_view.onclick = preview;
btn_save.onclick = save;

// Functions
// Update crossword pattern
function update() {
    crossword = qs_arr[idx];
    cw_locs = crossword.locations;
    cw_center = crossword.dimensions;
    cw_cross = crossword.cross;
    cw_down = crossword.down;
    cw_ordering = crossword.ordering;
    cw_words = Object.values(cw_cross).concat(Object.values(cw_down));
    clearHint();
    createHint();
//    for (var word of Object.values(cw_cross)) {
//        createInputTag(word);
//    }
//    for (var word of Object.values(cw_down)) {
//        createInputTag(word);
//    }
}

function save() {
    saveHint();
    viewHint();
}

function clearHint() {
    while (left.firstChild) {
        left.removeChild(left.lastChild);
    }
}

function createHint() {
    for (var word of cw_words) {
        let label = document.createElement('label');
        let prompt = document.createElement('input');
        label.textContent = word;
        label.setAttribute('for', word);
        prompt.type = "text";
        prompt.id = word;
        prompt.placeholder = "Hint";
        if (hints[word]) {prompt.value = hints[word]};
        left.appendChild(label);
        left.appendChild(prompt);
        left.appendChild(document.createElement("br"));
    }
}

function saveHint() {
    left.querySelectorAll("input").forEach((t) => {if (t.value && t.value != hints[t.id]) {hints[t.id] = t.value}});
    console.log(hints);
}

function clearCross() {
    while (cross.childElementCount > 1) {
        cross.removeChild(cross.lastChild);
    }
}

function clearDown() {
    while (down.childElementCount > 1) {
        down.removeChild(down.lastChild);
    }
}

function viewHint() {
    clearCross();
    clearDown();
    for (var [loc, word] of Object.entries(cw_cross)) {
        if (Object.keys(hints).includes(word)) {
            let p = document.createElement('p');
            let num = document.createElement('span');
            let txt = document.createElement('span');
            num.textContent = cw_ordering[loc];
            txt.textContent = '    ' + hints[word];
            p.appendChild(num).className = "order";
            p.appendChild(txt);
            cross.appendChild(p);
        }
    }
    for (var [loc, word] of Object.entries(cw_down)) {
        if (Object.keys(hints).includes(word)) {
            let p = document.createElement('p');
            let num = document.createElement('span');
            let txt = document.createElement('span');
            num.textContent = cw_ordering[loc];
            txt.textContent = '    ' + hints[word];
            p.appendChild(num).className = "order";
            p.appendChild(txt);
            down.appendChild(p);
        }
    }
}


// Navigation
function next() {
    idx = (idx + 1 ) % qs_arr.length;
    update();
    console.log(crossword);
    makeGrid();
}

function prev() {
    idx = (idx - 1) % qs_arr.length;
    if (idx < 0) {
        idx += qs_arr.length
    }
    update();
    console.log(crossword);
    makeGrid();
}

// Make grid
function makeGrid() {
    grid.style.setProperty('--grid-rows', grid_size);
    grid.style.setProperty('--grid-cols', grid_size);
    clearGrid();
    for (i = 0; i < grid_size; i++) {
        for (j = 0; j < grid_size; j++) {
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
    display_locs = transform(cw_locs);
    for (var key in display_locs) {
        if (document.getElementById(key)) {
            let cell = document.getElementById(key);
            cell.textContent = display_locs[key];
        }
    }
}

// Transformers
// Always put the crossword in the middle of the display
function transform(locs) {
    let grid_center = Math.floor((grid_size - 1) / 2);
    let x_diff = grid_center - cw_center[0];
    let y_diff = grid_center - cw_center[1];
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

// Increment grid size
function plus() {
    grid_size += 1;
    makeGrid();
}

// Decrement grid size
function minus() {
    if (grid_size > 5) {
        grid_size -= 1;
        makeGrid();
    }
}

// Preview
function preview() {
    if (!preview_mode) {
        clearGrid()
        for (i = 0; i < grid_size; i++) {
            for (j = 0; j < grid_size; j++) {
                let cell = document.createElement('div');
                cell.id = '' + i + ',' + j;
                if (cell.id in display_locs) {
                grid.appendChild(cell).className = 'grid-item';
                } else {
                grid.appendChild(cell).className = 'grid-item fade';
                }
            }
        }
        display_ordering = transform(cw_ordering);
        for (var key in display_ordering) {
            let cell = document.getElementById(key);
            if (!cell) {continue;}
            let ord = document.createElement('div');
            ord.textContent = display_ordering[key];
            cell.appendChild(ord).className = 'numberCircle';
        }
        preview_mode = 1;
        cross.setAttribute("style", "visibility:visible");
        down.setAttribute("style", "visibility:visible");
    } else {
        makeGrid();
        preview_mode = 0;
        cross.setAttribute("style", "visibility:hidden");
        down.setAttribute("style", "visibility:hidden");
    }
}

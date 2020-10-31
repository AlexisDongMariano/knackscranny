const pages = document.querySelectorAll('.test');
const btn_itemLabel = document.querySelector('.btn-item-label');
const chkbox_show_nw = document.querySelector("input[value=NW]");
const chkbox_show_sl = document.querySelector("input[value=SL]");
const chkbox_show_bs = document.querySelector("input[value=BS]");
const chkbox_show_sd = document.querySelector("input[value=SD]");

// initialize query
const itemsQuery = getFilters();

// get filter object from the local storage
function getFilters(){
    const itemsQuery = localStorage.getItem('filters');
    if(itemsQuery !== null)
        return JSON.parse(itemsQuery);
    else
        return [];
}

// save the filter to local storage
function saveFilter(queryObject){
    localStorage.setItem('filters', JSON.stringify(queryObject));
}


// add filter query
function addFilter(itemLabel){
    itemsQuery.push(
        itemLabel
    );
    saveFilter(itemsQuery);
}

// remove filter query
function removeFilter(itemLabel){
    const index = itemsQuery.indexOf(itemLabel);
    itemsQuery.splice(index, 1);
    saveFilter(itemsQuery);
}



chkbox_show_nw.addEventListener('change', e => {
    // if(e.target.checked)
    //     addFilter('NW');
    // else{
    //     removeFilter('NW');
    // }
    // console.log('FILTERS:', itemsQuery);
    if(location.search === '')
        location.assign(`${location.pathname}?filter=NW`);
    else
    location.assign(`${location.pathname}${location.search}&filter=NW`);
    
});

chkbox_show_sl.addEventListener('change', e => {
    if(e.target.checked)
        addFilter('SL');
    else{
        removeFilter('SL');
    }
    console.log('FILTERS:', itemsQuery);
});

chkbox_show_bs.addEventListener('change', e => {
    if(e.target.checked)
        addFilter('BS');
    else{
        removeFilter('BS');
    }
    console.log('FILTERS:', itemsQuery);
});

chkbox_show_sd.addEventListener('change', e => {
    if(e.target.checked)
        addFilter('SD');
    else{
        removeFilter('SD');
    }
    console.log('FILTERS:', itemsQuery);
});









let test = '';
let search = '';
pages.forEach(page => {
if(location.search.indexOf('search') !== -1){
    search = location.search.substring(location.search.indexOf('search'));
    page.href = `${page.href}&${search}`;
}   
console.log('updated:', page.href);
});




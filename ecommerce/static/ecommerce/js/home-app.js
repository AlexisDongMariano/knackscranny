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

// add filter to local storage
function addFilter(itemLabel){
    itemsQuery.push(
        itemLabel
    );
    localStorage.setItem('filters', JSON.stringify(itemsQuery));
}


console.log('items query:', itemsQuery, typeof(itemsQuery));
console.log(chkbox_show_nw );







let test = '';
let search = '';
pages.forEach(page => {
if(location.search.indexOf('search') !== -1){
    search = location.search.substring(location.search.indexOf('search'));
    page.href = `${page.href}&${search}`;
}   
console.log('updated:', page.href);
});




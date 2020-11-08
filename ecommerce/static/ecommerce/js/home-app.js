// ==============================
//         UI ELEMENTS
// ==============================

const pages = document.querySelectorAll('.test');
const btn_itemLabel = document.querySelector('.btn-item-label');
const chkbox_show_nw = document.querySelector("input[value=NW]");
const chkbox_show_sl = document.querySelector("input[value=SL]");
const chkbox_show_bs = document.querySelector("input[value=BS]");
const chkbox_show_sd = document.querySelector("input[value=SD]");


// ==============================
//         GLOBAL VARIABLES
// ==============================

const itemsQuery = getFilters();
const filterQueries = itemsQuery[0];
let searchGlobal = location.search;
let prevURL = '';
if(document.referrer !== '')
    prevURL = new URL(document.referrer);



// ==============================
//         EVENT LISTENERS
// ==============================

chkbox_show_nw.addEventListener('change', e => {
    setFilter('NW');
});

chkbox_show_sl.addEventListener('change', e => {
    setFilter('SL');
});

chkbox_show_bs.addEventListener('change', e => {
    setFilter('BS');
});

chkbox_show_sd.addEventListener('change', e => {
    setFilter('SD');
});


// ==============================
//         GLOBAL FUNCTIONS
// ==============================

// get filter object from the local storage
function getFilters(){
    const itemsQuery = localStorage.getItem('filters');

    if(itemsQuery !== null){
        return JSON.parse(itemsQuery);
    }
    else{
        return [{
            NW: false,
            SL: false,
            BS: false,
            SD: false
        }];
    }     
}

// save the filter to local storage
function saveFilter(queryObject){
    localStorage.setItem('filters', JSON.stringify(queryObject));
}

// add/set filter query
function setFilter(itemLabel){
    if(itemLabel === 'NW')
        filterQueries.NW = !filterQueries.NW;
    else if(itemLabel === 'SL')
        filterQueries.SL = !filterQueries.SL;
    else if(itemLabel === 'BS')
        filterQueries.BS = !filterQueries.BS;
    else if(itemLabel === 'SD')
        filterQueries.SD = !filterQueries.SD;

    saveFilter(itemsQuery);
    // redirect or render the page upon checkbox change
    location.assign(`${location.pathname}${generateSearchUrl(2)}`);
}

// searchType 1: pages and search
// searchType 2: filter
function generateSearchUrl(searchType) {
    const filterQueries = itemsQuery[0];
    let search = '';

    // generate search url for the pagination a href buttons
    if(searchType === 1){
        // if we found the search keyword in url, we will append & and the remaining search in url starting from
        // the search keyword else if it starts with filter keyword, we'll do the same but with filter keyword
        // else, the returning search will be blank
        if(location.search.indexOf('search') !== -1)
            search = '&' + location.search.substring(location.search.indexOf('search'));
        else if(location.search.indexOf('filter') !== -1){
            search = '&' + location.search.substring(location.search.indexOf('filter'));    
        }
        else
            search = '';

        return search;
    }
    // generate search url if any filter box was checked
    if(searchType === 2){
        arr_search = searchGlobal.split('&');
        console.log('INSIDE generate search url, arr_search:', arr_search);
        // check the search url if it already contains page keywords as we will remove it and use
        // appropriate prefix (&, ?) for the filter keywords
        const pageIndex = arr_search.findIndex(element => {
            return element.startsWith('&page') || element.startsWith('?page');
        });

        if(pageIndex > -1)
            arr_search.splice(pageIndex, 1);

        search = arr_search.join('&');

        if(!search.startsWith('?') && !search.startsWith('&') && search !== '')
            search = '?' + search;
        else if(search.startsWith('&'))
            search = search.substring(1, search.length);

        for(let key in filterQueries){
            console.log('INSIDE loop, search:', search);
            if(search !== ''){
                // getting the search and refreshing to remove the page in search terms
                if(filterQueries[key]){
                    let x = search.indexOf(`?filter=${key}`);
                    let y = search.indexOf(`&filter=${key}`);

                    if(x === -1 && y === -1)
                        search += `&filter=${key}`;
                }
                else{
                    search = search.replace(`?filter=${key}`, '');
                    search = search.replace(`&filter=${key}`, ''); 

                    if(search.charAt(0) === '&')
                        search = search.replace(search.charAt(0), '?'); 
                }
            }
            else{
                if(filterQueries[key]){
                    search = `?filter=${key}`;
                }
            }  
        }
        console.log('BEFORE RETURNING SEARCH:', search);
        return search;
    }  
}


// ==============================
//         RUNTIME LOGIC
// ==============================

// generate href of pages/pagination buttons
pages.forEach(page => {
    page.href = `${page.href}${generateSearchUrl(1)}`;
    console.log('updated:', page.href);
});

// if the previous first pathname is not home, clear the filter checkboxes
if(prevURL.pathname.split('/')[1] !== 'home'){
    filterQueries.NW = false;
    filterQueries.SL = false;
    filterQueries.BS = false;
    filterQueries.SD = false;
}

// if a filter checkbox is checked, add the filters to the search property of the location
let reload = false;
for(let key in filterQueries){
    if(filterQueries[key]){
        if(location.search.indexOf('filter') === -1){
            reload = true;
        }
    }
}

if(reload)
    location.assign(`${location.pathname}${generateSearchUrl(2)}`);

// set the checkbox status based on value in localStorage
chkbox_show_nw.checked = itemsQuery[0].NW;
chkbox_show_sl.checked = itemsQuery[0].SL;
chkbox_show_bs.checked = itemsQuery[0].BS;
chkbox_show_sd.checked = itemsQuery[0].SD;









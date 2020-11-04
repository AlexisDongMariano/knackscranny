const pages = document.querySelectorAll('.test');
const btn_itemLabel = document.querySelector('.btn-item-label');
const chkbox_show_nw = document.querySelector("input[value=NW]");
const chkbox_show_sl = document.querySelector("input[value=SL]");
const chkbox_show_bs = document.querySelector("input[value=BS]");
const chkbox_show_sd = document.querySelector("input[value=SD]");

// initialize query
const itemsQuery = getFilters();
let searchGlobal = location.search;

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
    const filterQueries = itemsQuery[0];

    if(itemLabel === 'NW')
        filterQueries.NW = !filterQueries.NW;
    else if(itemLabel === 'SL')
        filterQueries.SL = !filterQueries.SL;
    else if(itemLabel === 'BS')
        filterQueries.BS = !filterQueries.BS;
    else if(itemLabel === 'SD')
        filterQueries.SD = !filterQueries.SD;

    saveFilter(itemsQuery);
    location.assign(`${location.pathname}${generateSearchUrl(2)}`);
}

// remove filter query
function removeFilter(itemLabel){
    const index = itemsQuery.indexOf(itemLabel);
    itemsQuery.splice(index, 1);
    saveFilter(itemsQuery);
}

// searchType 1: pages and search
// searchType 2: filter
function generateSearchUrl(searchType) {
    const filterQueries = itemsQuery[0];
    let search = '';
    debugger;

    if(searchType === 1){
        if(location.search.indexOf('filter') !== -1){
            if(searchGlobal.startsWith('?'))
                search = '&' + searchGlobal.substring(1);
            else
                search = searchGlobal;
            debugger
        }
        else if(location.search.indexOf('search') !== -1)
            search = '&' + location.search.substring(location.search.indexOf('search'));
        else
            search = '';
        debugger;
        return search;
    }
    // generate search url if any filter box was checked
    if(searchType === 2){
        arr_search = searchGlobal.split('&');
        console.log('2search:', arr_search);

        const pageIndex = arr_search.findIndex(element => {
            return element.startsWith('&page') || element.startsWith('?page');
        });

        console.log(pageIndex);
        if(pageIndex > -1)
            arr_search.splice(pageIndex, 1);

        console.log('3search:', arr_search);
        search = arr_search.join('&');
        console.log('4search:', search);
        if(!search.startsWith('?') && !search.startsWith('&') && search !== ''){
            search = '?' + search;
            console.log('1');
        }
        else if(search.startsWith('&')){
            search = search.substring(1,search.length);
            console.log('2');
        }
        console.log('NEW SEARCH:', search);
        console.log('1search:', searchGlobal);
        for(let key in filterQueries){
            console.log(key, filterQueries[key]);
            if(searchGlobal && search !== ''){
                // getting the search and refreshing to remove the page in search terms
                if(filterQueries[key]){
                    console.log('1x');
                    let x = search.indexOf(`?filter=${key}`);
                    let y = search.indexOf(`&filter=${key}`);

                    if(x === -1 && y === -1){
                        search += `&filter=${key}`;
                        console.log('2x');
                    }
                    console.log('3x');
                }
                else{
                    search = search.replace(`?filter=${key}`, '');
                    search = search.replace(`&filter=${key}`, ''); 
                    console.log('4x');
                    if(search.charAt(0) === '&'){
                        search = search.replace(search.charAt(0), '?'); 
                        console.log('5x');
                    }
                    console.log('6x');    
                }
            }
            else{
                if(filterQueries[key]){
                    search = `?filter=${key}`;
                }
            }  
        }
        console.log('search:', search);
        return search;
    }
    
}

// generate href of pages/pagination buttons
pages.forEach(page => {
    page.href = `${page.href}${generateSearchUrl(1)}`;
    console.log('updated:', page.href);
});


// EVENT LISTENERS
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


// set the checkbox status based on value in localStorage
chkbox_show_nw.checked = itemsQuery[0].NW
chkbox_show_sl.checked = itemsQuery[0].SL
chkbox_show_bs.checked = itemsQuery[0].BS
chkbox_show_sd.checked = itemsQuery[0].SD









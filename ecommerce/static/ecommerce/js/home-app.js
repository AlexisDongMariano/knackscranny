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
    let search = location.search;
 
    if(itemLabel === 'NW')
        filterQueries.NW = !filterQueries.NW;
    else if(itemLabel === 'SL')
        filterQueries.SL = !filterQueries.SL;
    else if(itemLabel === 'BS')
        filterQueries.BS = !filterQueries.BS;
    else if(itemLabel === 'SD')
        filterQueries.SD = !filterQueries.SD;

    saveFilter(itemsQuery);

    // // generate filter url local function
    // const generateFilterURL = itemsQuery
    console.log('search:', search);
    for(let key in filterQueries){
        console.log(key, filterQueries[key]);
        if(search){
            console.log('search exists');
            if(filterQueries[key]){
                console.log('will add the label');
                console.log('before adding label:', search);
                console.log(`currence of &${key}:`, search.indexOf(`&filter=${key}`));
                console.log(`currence of ?${key}:`, search.indexOf(`?filter=${key}`));

                let x = search.indexOf(`?filter=${key}`);
                let y = search.indexOf(`&filter=${key}`);
                console.log('x:', x, 'y:', y);

                if(x === -1 && y === -1)
                    console.log('WALA PA');
                else
                    console.log('MERON NA');

                if(x === -1 && y === -1){
                    console.log('label is not yet found');
                    search += `&filter=${key}`;
                }
                else{
                    console.log('TANGINA EXECUTE NATIN TO');
                }
                console.log('after checking label:', search);
            }
            else{
                console.log('will remove the label');
                search = search.replace(`?filter=${key}`, '');
                search = search.replace(`&filter=${key}`, ''); 

                if(search.charAt(0) === '&')
                    search = search.replace(search.charAt(0), '?'); 
            }
        }
        else{
            console.log('search does not exists');
            if(filterQueries[key]){
                console.log('setting search');
                search = `?filter=${key}`;
            }
        }
            
    }
    console.log('search:', search);
    location.assign(`${location.pathname}${search}`);
}

// remove filter query
function removeFilter(itemLabel){
    const index = itemsQuery.indexOf(itemLabel);
    itemsQuery.splice(index, 1);
    saveFilter(itemsQuery);
}






// EVENT LISTENERS
chkbox_show_nw.addEventListener('change', e => {
    // if(e.target.checked){
    //     console.log('this is called 1');
    //     if(location.search === '')
    //         location.assign(`${location.pathname}?filter=NW`);
    //     else
    //         location.assign(`${location.pathname}${location.search}&filter=NW`);
    // }
    // else{
    //     console.log(`${location.pathname}${location.search}&filter=NW`);
    //     location.assign(`${location.pathname}${location.search}&filter=NW`);
    //     console.log('this is called 2');
    //     location.assign(`${location.pathname}`);
    // }
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





let test = '';
let search = '';
pages.forEach(page => {
if(location.search.indexOf('search') !== -1){
    search = location.search.substring(location.search.indexOf('search'));
    page.href = `${page.href}&${search}`;
}   
console.log('updated:', page.href);
});




// const searchBtn = document.getElementById('s-b-s-btn');
// searchBtn.addEventListener('click',fetchData);

// function fetchData(e){
//     e.preventDefault();
//     let userInput= document.getElementById('search-input');
//     let texty = userInput.value
//     let searchText = texty.replace(" ", "%20")
//     const username = ""
//     const password = ""
//     let endpoint = `https://www.nutritics.com/api/v1.1/LIST/food=${searchText}`
    
//     var headers = new Headers();

//     headers.append('Authorization', 'Basic ' + window.btoa('ayoubamk123' + ':' + 'aitlaman1'));

//     headers.append('Content-Type', 'application/json');
//     headers.append('Accept', 'application/json');
  
//     headers.append('Access-Control-Allow-Origin', 'http://127.0.0.1:5000/');
//     headers.append('Access-Control-Allow-Credentials', 'true');
  
//     headers.append('GET', 'POST', 'OPTIONS');
    
//     document.getElementById('nut-results').style.display="none";
//     document.getElementById('loader').style.display = 'block';
//     window.setTimeout(closeLoader, 4000);

//     fetch(endpoint, {headers: headers}).then(response => {
//         if(response.ok){
//             return response.json();
//          } 
//     })
//     .then(data => {
//         let container = '';
//         for(let i = 1 ; i <= 3 ; i++){
//             container =  container + ` <a href=${data[i.toString()]["reporturl"]} target="_blank">
//                      <div class="res-card">
//                            <div id="item-photo">
//                                 <img src=${data[i.toString()]["photo"]}>
//                            </div>
//                            <div id="item-info">
//                                  <h4>${data[i.toString()]["name"]}</h4>
//                                  <p>${data[i.toString()]["cat"]}</p>
//                            </div>
//                      </div>
//              </a>`;
//         }
//         document.getElementById('nut-results').innerHTML = container;
        
//    }
//        );
// }

// function closeLoader() {
//     document.getElementById('loader').style.display = 'none';
//     document.getElementById('nut-results').style.display="block";
// }
        


const searchBtn = document.getElementById('s-b-s-btn');
searchBtn.addEventListener('click',redirect);
function redirect(e) {
    e.preventDefault();
    let userInput= document.getElementById('search-input');
    let texty = userInput.value
    let searchText = texty.replace(" ", "%20")  
    window.open(
        `https://www.calorieking.com/us/en/foods/search?keywords=${searchText}`,
        '_blank' 
      );
    }


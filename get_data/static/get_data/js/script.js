// Request last price data

// v1
// async function loadRTData() {
setInterval(async function loadRTData() {
    const response = await fetch('http://127.0.0.1:8500/api/rt_data');
    
    if (!response.ok) {
        const message = `An error has occured: ${response.status}`;
        throw new Error(message);
      }
    
    const lastPrice = await response.json();
    // console.log(lastPrice);
    // console.log(typeof lastPrice);
    // Fronend deploy
    // Light when something chanching
    for (el in lastPrice) {
        // document.getElementById(lastPrice[el]['symbol'] + "_price").innerHTML= [el]['last_price'];
        // Last Price
        asset = lastPrice[el]['symbol']
        // console.log(asset);
        var price = document.getElementById(asset + "_price");
        price.innerHTML = lastPrice[el]['last_price']
        // console.log(price)
        // Amount of Position
        var amount = document.getElementById(asset + "_amount");
        amount.innerHTML = lastPrice[el]['amount_of_position'];
        // Futures Position
        var amount = document.getElementById(asset + "_fut_pos");
        amount.innerHTML = lastPrice[el]['futures_pos'];
        // Max position % stop
        var amount = document.getElementById(asset + "_stop_prc");
        amount.innerHTML = lastPrice[el]['max_prc_stop'];
        // ATR percent passed (has moved from the open)
        var atr_prc = document.getElementById(asset + "_atr_prc");
        atr_prc.innerHTML = lastPrice[el]['atr_prc_passed'];
        // Releative Position on 2 Last sessions
        var two_ses = document.getElementById(asset + "_two_ses");
        two_ses.innerHTML = lastPrice[el]['today_two_ses'];
    }


    return lastPrice;
// };
}, 30000);
// loadRTData()

// v4 pure promise syntax
// setInterval(function loadRTData() {
//     fetch('http://127.0.0.1:8500/api/rt_data')
//     .then(response => response.json())
//     .then(commits => console.log(commits));
//     // .then(commits => alert(commits));
    
// }, 30000)       // 30 sec
// loadRTData()

// v2
// async function loadRTData() {
//     while(1) {
//         await fetch("http://127.0.0.1:8500/api/rt_data");
//         await new Promise(res => setTimeout(res, 1000));

//         const lp = res.json()
//         console.log(lp);
//   }
// };
// loadRTData()




// v3
// async function subscribe() {
//   let response = await fetch("http://127.0.0.1:8500/api/rt_data");

//   if (response.status == 502) {
//     // Status 502 is a connection timeout error,
//     // may happen when the connection was pending for too long,
//     // and the remote server or a proxy closed it
//     // let's reconnect
//     await subscribe();
//   } else if (response.status != 200) {
//     // An error - let's show it
//     // showMessage(response.statusText);
//     // Reconnect in one second
//     await new Promise(resolve => setTimeout(resolve, 1000));
//     await subscribe();
//   } else {
//     // Get and show the message
//     let message = await response.text();
//     // showMessage(message);
//     // Call subscribe() again to get the next message
//     await subscribe();
//   }
// }

// subscribe();
// setInterval(subscribe(), 2000);





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
    // Fronend deploy
    // Light when something chanching
    for (el in lastPrice) {
        // document.getElementById(lastPrice[el]['symbol'] + "_price").innerHTML= [el]['last_price'];
        // Last Price
        asset = lastPrice[el]['symbol']
        var price = document.getElementById(asset + "_price");
        price.innerHTML = lastPrice[el]['last_price']
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
        var atr_prc_scale = document.getElementById(asset + "_atr_prc_scale");
        atr_prc_scale.value = lastPrice[el]['atr_prc_passed'];
        // Releative Position on 2 Last sessions
        var two_ses = document.getElementById(asset + "_two_ses");
        two_ses.innerHTML = lastPrice[el]['today_two_ses'];
        // ATRs levels
        var half_atr = document.getElementById(asset + "_half_atr");
        half_atr.innerHTML = lastPrice[el]['atr_levels'][1];
        var three_quarter_atr = document.getElementById(asset + "_three_quarter_atr");
        three_quarter_atr.innerHTML = lastPrice[el]['atr_levels'][2];
        var point_atr = document.getElementById(asset + "_point_atr");
        point_atr.innerHTML = lastPrice[el]['atr_levels'][3];
        // Yesterday Body Level
        var ysd_body_level = document.getElementById(asset + "_ysd_body_level");
        ysd_body_level.innerHTML = lastPrice[el]['ysd_body_level'];
        var ysd_tail = document.getElementById(asset + "_ysd_tail");
        ysd_tail.innerHTML = lastPrice[el]['ysd_tail'];
        var ysd_body_border = document.getElementById(asset + "_ysd_body_border");
        ysd_body_border.innerHTML = lastPrice[el]['ysd_body_border'];
        
        // Maching levels
        var atr_day_prc = 10;
        var difForCompare = atr_day_prc/25000;     // coz this is %
        var levels_atr = lastPrice[el]['atr_levels']
        for (level in levels_atr) {
            console.log(lastPrice[el]['atr_levels'][level])
            if ( (levels_atr[level]*difForCompare)+levels_atr[level] ) {

            }
        }
    }

    // return lastPrice;
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





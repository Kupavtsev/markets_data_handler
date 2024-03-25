// Request last price data




// v4 pure promise syntax
setInterval(function loadRTData() {
    fetch('http://127.0.0.1:8500/api/rt_data')
    .then(response => response.json())
    .then(commits => console.log(commits));
    // .then(commits => alert(commits));
    
}, 30000)       // 30 sec
// setInterval(loadRTData(), 5000);
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


// v1
// async function loadRTData() {
//     const response = await fetch('http://127.0.0.1:8500/api/rt_data');
    
//     if (!response.ok) {
//         const message = `An error has occured: ${response.status}`;
//         throw new Error(message);
//       }
    
//     const lastPrice = await response.json();
//     console.log(lastPrice);
//     return lastPrice;
// }
// // setInterval(loadRTData(), 1000);
// loadRTData()

// v2
// async function loadRTData() {
//     while(1) {
//         await fetch("http://127.0.0.1:8500/api/rt_data");
//         await new Promise(res => setTimeout(res, 1000));

//         const lp = res.json()
//         console.log(lp);
//   }
// }
// loadRTData()

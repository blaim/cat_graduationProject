const items = [
    {name:"Rice", price:5},
    {name:"Book", price:20},
    {name:"Chicken", price:10},
    {name:"Monitor", price:100},
]

// 리턴하는 값은 한 iteration마다 total에 저장됨
//마지막에 totalPrice로 리턴
//두번째 요소 하나
const totalPrice = items.reduce((total, item)=>{

    return total + item.price
   //시작값 
}, 0)

console.log(totalPrice)
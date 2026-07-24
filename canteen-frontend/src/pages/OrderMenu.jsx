import { useParams } from "react-router-dom";
import { useEffect, useState } from 'react';
import axios from 'axios';
function OrderMenu() {

    const { session_id } = useParams();
    const [menuItems, setMenuItems] = useState([]);
    const user = JSON.parse(localStorage.getItem("user"));
    useEffect(() => {
    async function fetchMenuItems() {
        try {
            const response = await axios.get(
                `http://localhost:5000/menu/${session_id}`
            );

            setMenuItems(response.data);
        } catch (error) {
            console.error("Error fetching menu items:", error);
        }
    }

    fetchMenuItems();
}, [session_id]);
    console.log(menuItems);

   async function handleAddToCart(item) {
        const data = {
        student_id: user.user_id,
        menu_item_id: item.item_id,
        quantity: 1,
        meal_session_id: session_id
    };

    try {
       const response = await axios.post("http://localhost:5000/cart/add",data)
       alert(response.data.message);
    }catch (error) {
        console.error(error);
    }
    
}
    return (
    <>
        <h1>Order Menu</h1>

        {menuItems.map((item) => {
            return (
                <div key={item.item_id}>
                    <h3>{item.item_name}</h3>
                    <p>₹{item.price}</p>
                    <button onClick= {() => handleAddToCart(item)}>
                        Add to Cart
                    </button>
                </div>
            );
        })}
    </>
);
}
export default OrderMenu;
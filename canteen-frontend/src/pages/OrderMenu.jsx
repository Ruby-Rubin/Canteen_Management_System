import { useParams } from "react-router-dom";
import { useEffect, useState } from 'react';
import axios from 'axios';
function OrderMenu() {

    const { session_id } = useParams();
    const [menuItems, setMenuItems] = useState([]);
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

    function handleAddToCart(item) {

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
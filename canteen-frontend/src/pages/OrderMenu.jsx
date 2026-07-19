import { useParams } from "react-router-dom";

function OrderMenu() {

    const { session_id } = useParams();

    console.log(session_id);

    return (
        <h1>Order Menu</h1>
    );
}
export default OrderMenu;
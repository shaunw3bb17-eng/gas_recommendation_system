import { useState } from 'react'
import './App.css'

function App(){

  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [bestStation, setBestStation] = useState(null);

  async function findBestStation() {
    
    try{
      const response = await fetch(
      `http://127.0.0.1:8000/best_station?lat=${latitude}&lon=${longitude}`
   );



   console.log("Response.status:", response.status) 
    

    const data = await response.json();

    console.log("Data received:",data);

    setBestStation(data);
  }catch (error){
      console.error("Fetch error:",error);
    }
  }

  return(
    <div>
      <h1> Gas Price Recommendation System</h1>

      <p>Welcome to the Jamaican gas station Recommendation System</p>

      <p> Frontend connected to FastAPI backend.</p>

      <div>
        <label>Latitude</label>
        <br />

        <input
         type = "text"
         value = {latitude}
         onChange={(e) => setLatitude(e.target.value)}
         />
         <br />
         <br />

         <label>Longitude</label>
         <br />

         <input
         type = "text"
         value = {longitude}
         onChange={(e) => setLongitude(e.target.value)}
         />
         <br />
         <br />

         <button onClick= {findBestStation}>
          Find best station
         </button>
         {bestStation &&(
          <div>
            <h2>Recommendation</h2>

            <p>Best Station: {bestStation.best_station}</p>
            <p>Price: J${bestStation.current_price}</p>
            <p>Distance: {bestStation.distance_km} km</p>
            <p>Traffic: {bestStation.traffic}</p>
            <p>score: {bestStation.score}</p>
            </div>
         )}
      </div>

    </div>
  );
}
export default App
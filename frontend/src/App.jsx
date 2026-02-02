import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

function App() {
  return (
    <>
      <Navbar />
      <div className="container mx-auto p-8 h-full">
        <Home />
      </div>
      <Footer />
    </>
  );
}

export default App;

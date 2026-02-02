import { useState } from "react";
import AxiosInstance from "../hooks/axios.js";
import ImageCard from "../components/ImageCard.jsx";

function Home() {
  const [caption, setCaption] = useState("");
  const [image, setImage] = useState(null);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    if (caption !== "") {
      AxiosInstance.post("/api/search/", {
        type: "caption",
        caption: caption,
        k: 3,
      })
        .then((res) => setImages(res.data.results || []))
        .catch((err) => console.error("Caption search error:", err))
        .finally(() => setLoading(false));
    }

    if (image) {
      const formData = new FormData();
      formData.append("type", "image");
      formData.append("image", image);

      AxiosInstance.post("/api/search/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
        .then((res) => setImages(res.data.results))
        .catch((err) => console.error("Image search error:", err))
        .finally(() => setLoading(false));
    }
  };

  return (
    <div className="flex flex-col items-center h-full gap-y-12">
      <h3 className="text-xl font-medium mt-6">
        Search for images by uploading an image or entering a caption.
      </h3>

      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <div className="flex gap-x-6 mb-8">
          <input
            type="text"
            className="border border-gray-300 p-2 rounded-lg w-80"
            placeholder="Enter caption here..."
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            hidden={image != null}
          />

          <input
            type="file"
            accept="image/*"
            className="border border-gray-300 p-2 rounded-lg w-56"
            onChange={(e) => setImage(e.target.files[0])}
            hidden={caption !== ""}
          />
        </div>

        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 cursor-pointer duration-200 text-white w-full p-2.5 rounded-lg"
        >
          Search
        </button>
      </form>

      <div className="grid grid-cols-3 gap-6 mt-4">
        {loading ? (
          <p>Loading...</p>
        ) : images && images.length === 0 ? (
          <p>No results found.</p>
        ) : (
          images.map((item, index) => <ImageCard key={index} item={item} />)
        )}
      </div>
    </div>
  );
}

export default Home;

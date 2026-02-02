function ImageCard({ item }) {
  const imageUrl = `http://127.0.0.1:8000${item.path || item.image}`;

  return (
    <div className="w-56 p-3 bg-white shadow-md rounded-xl flex flex-col items-center">
      <img
        src={imageUrl}
        alt={item.name || ""}
        className="w-44 h-60 object-cover mb-3 rounded-lg"
      />
    </div>
  );
}

export default ImageCard;

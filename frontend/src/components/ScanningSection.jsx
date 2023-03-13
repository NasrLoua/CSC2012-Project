import React from 'react';
import { useState } from 'react';

export default function ScanningSection() {
  const [imageSrc, setImageSrc] = useState(null);

  function handleFileInputChange(event) {
    const file = event.target.files[0];

    const reader = new FileReader();
    reader.onload = function (e) {
      setImageSrc(e.target.result);
    };
    reader.readAsDataURL(file);

  }

  function handleRemoveImage() {
    setImageSrc(null);
  }
  
  return (
    <div className="bg-white rounded-lg shadow-2xl p-4 h-full">
      <h2 className="text-lg font-medium mb-4">Scanning Section</h2>
      {/* Insert scanning section content here */}

      {imageSrc ? (
        <div className="relative">
          <img src={imageSrc} alt="Selected image" className="max-w-full max-h-full" />
          <button className="absolute top-2 right-2 p-2 rounded-full bg-red-500 text-white" onClick={handleRemoveImage}>
            <span className="sr-only">Remove image</span>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
              <path
                fillRule="evenodd"
                d="M10 1.667c-4.142 0-7.5 3.358-7.5 7.5s3.358 7.5 7.5 7.5 7.5-3.358 7.5-7.5-3.358-7.5-7.5-7.5zm3.535 10.607a.75.75 0 0 1 0 1.06.75.75 0 0 1-1.06 0L10 11.06l-2.475 2.475a.75.75 0 0 1-1.06 0 .75.75 0 0 1 0-1.06L8.94 10l-2.475-2.475a.75.75 0 0 1 1.06-1.06L10 8.94l2.475-2.475a.75.75 0 0 1 1.06 1.06L11.06 10l2.475 2.475z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>
      ) : (
        <div>
          <p className="mb-2">Select an image to display it here:</p>
          <input type="file" accept="image/*" onChange={handleFileInputChange} />
        </div>
      )}

    </div>
  );
}
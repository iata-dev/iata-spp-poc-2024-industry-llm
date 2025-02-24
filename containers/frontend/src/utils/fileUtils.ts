import imageCompression from "browser-image-compression";

export const compressImage = async (file: File): Promise<File> => {
  if (!file.type.startsWith("image/")) {
    return file;
  }

  const options = {
    maxSizeMB: 1,
    maxWidthOrHeight: 1920,
    useWebWorker: true,
  };

  try {
    return await imageCompression(file, options);
  } catch (error) {
    console.error("Error compressing image:", error);
    return file;
  }
};

export const fileToBase64 = (file: File): Promise<string> => {
  return new Promise(async (resolve, reject) => {
    try {
      const compressedFile = await compressImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result as string;
        resolve(base64String);
      };
      reader.onerror = reject;
      reader.readAsDataURL(compressedFile);
    } catch (error) {
      reject(error);
    }
  });
};

export const getCleanBase64 = (dataUrl: string): string => {
  const matches = dataUrl.match(/^data:([A-Za-z-+/]+);base64,(.+)$/);
  if (matches && matches.length === 3) {
    return matches[2]; // Return only the base64 data without the prefix
  }
  return dataUrl;
};

export const createCameraCaptureFile = (base64Data: string, fileName: string = "camera_capture.jpg") => {
  const dataUrl = base64Data.startsWith("data:") ? base64Data : `data:image/jpeg;base64,${base64Data}`;

  return {
    id: Date.now().toString() + Math.random(),
    name: fileName,
    data: dataUrl,
    type: "image/jpeg",
  };
};

export const createFileObject = (file: File, base64Data: string, id?: string) => {
  const dataUrl = base64Data.startsWith("data:") ? base64Data : `data:${file.type};base64,${base64Data}`;

  return {
    id: id || Date.now().toString() + Math.random(),
    name: file.name,
    data: dataUrl,
    type: file.type,
  };
};

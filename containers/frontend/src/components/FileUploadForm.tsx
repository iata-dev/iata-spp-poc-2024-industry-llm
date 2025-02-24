import React, { FormEvent, ChangeEvent, useRef } from "react";
import { SelectedFile } from "../types";

interface FileUploadFormProps {
  selectedFiles: SelectedFile[];
  onFileSelect: (e: ChangeEvent<HTMLInputElement>) => void;
  onCameraCapture: (e: ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
  onRemoveFile: (id: string) => void;
  isMobileOrTablet: boolean;
  isProcessing: boolean;
}

export const FileUploadForm: React.FC<FileUploadFormProps> = ({
  selectedFiles,
  onFileSelect,
  onCameraCapture,
  onSubmit,
  onRemoveFile,
  isMobileOrTablet,
  isProcessing = false,
}) => {
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: ChangeEvent<HTMLInputElement>) => {
    if (!isProcessing) {
      onFileSelect(e);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleCameraCapture = (e: ChangeEvent<HTMLInputElement>) => {
    if (!isProcessing) {
      onCameraCapture(e);
      if (cameraInputRef.current) {
        cameraInputRef.current.value = "";
      }
    }
  };

  return (
    <form onSubmit={onSubmit} className={`fixed bottom-0 left-0 right-0 bg-white pt-1 pb-2 ${isMobileOrTablet ? "" : "ml-64"}`}>
      <div className={`mx-auto ${isMobileOrTablet ? "w-[95%]" : "w-[90%] md:max-w-[70%]"}`}>
        <div className='bg-white rounded-xl shadow-sm border border-gray-200'>
          {selectedFiles.length > 0 && !isProcessing && (
            <div className='p-4 border-b'>
              <div className='flex flex-wrap gap-2'>
                {selectedFiles.map((file) => (
                  <div key={file.id} className='inline-flex items-center gap-2 px-3 py-2 bg-green-100 text-green-800 rounded-lg'>
                    <span className='text-sm font-medium'>{file.name}</span>
                    <button
                      type='button'
                      onClick={() => onRemoveFile(file.id)}
                      className='p-1 bg-white hover:bg-gray-50 rounded-full text-green-600 hover:text-green-800 transition-colors'
                    >
                      <svg
                        xmlns='http://www.w3.org/2000/svg'
                        fill='none'
                        viewBox='0 0 24 24'
                        strokeWidth={1.5}
                        stroke='currentColor'
                        className='w-5 h-5'
                      >
                        <path strokeLinecap='round' strokeLinejoin='round' d='M6 18L18 6M6 6l12 12' />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className='p-4 flex items-center gap-4'>
            <div className='flex gap-2'>
              <label
                className={`
                flex items-center justify-center p-2 
                ${isProcessing ? "opacity-50 cursor-not-allowed" : "hover:bg-gray-100 cursor-pointer"} 
                rounded-lg transition-colors
              `}
              >
                <input
                  ref={fileInputRef}
                  type='file'
                  accept='image/*, application/pdf'
                  onChange={handleFileSelect}
                  className='hidden'
                  multiple
                  disabled={isProcessing}
                />
                <svg
                  xmlns='http://www.w3.org/2000/svg'
                  fill='none'
                  viewBox='0 0 24 24'
                  strokeWidth={1.5}
                  stroke='currentColor'
                  className='w-6 h-6 text-gray-500'
                >
                  <path
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    d='M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13'
                  />
                </svg>
              </label>

              {isMobileOrTablet && (
                <label
                  className={`
                  flex items-center justify-center p-2 
                  ${isProcessing ? "opacity-50 cursor-not-allowed" : "hover:bg-gray-100 cursor-pointer"} 
                  rounded-lg transition-colors
                `}
                >
                  <input
                    ref={cameraInputRef}
                    type='file'
                    accept='image/*'
                    capture='environment'
                    onChange={handleCameraCapture}
                    className='hidden'
                    disabled={isProcessing}
                  />
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    fill='none'
                    viewBox='0 0 24 24'
                    strokeWidth={1.5}
                    stroke='currentColor'
                    className='w-6 h-6 text-gray-500'
                  >
                    <path
                      strokeLinecap='round'
                      strokeLinejoin='round'
                      d='M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z'
                    />
                    <path
                      strokeLinecap='round'
                      strokeLinejoin='round'
                      d='M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z'
                    />
                  </svg>
                </label>
              )}
            </div>

            {selectedFiles.length > 0 && !isProcessing && (
              <button
                type='submit'
                className='flex items-center justify-center ml-auto p-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors'
              >
                <svg
                  xmlns='http://www.w3.org/2000/svg'
                  fill='none'
                  viewBox='0 0 24 24'
                  strokeWidth={1.5}
                  stroke='currentColor'
                  className='w-5 h-5'
                >
                  <path
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    d='M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5'
                  />
                </svg>
              </button>
            )}
          </div>
        </div>
      </div>
    </form>
  );
};

export default FileUploadForm;

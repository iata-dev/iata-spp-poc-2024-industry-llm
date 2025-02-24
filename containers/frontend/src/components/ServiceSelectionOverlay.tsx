import React from "react";
import { ServiceSource } from "../types";

interface ServiceSelectionOverlayProps {
  onServiceSelect: (service: ServiceSource) => void;
  isMobileOrTablet: boolean;
}

const ServiceSelectionOverlay: React.FC<ServiceSelectionOverlayProps> = ({ onServiceSelect, isMobileOrTablet }) => {
  const topMargin = isMobileOrTablet ? "160px" : "64px";
  return (
    <div className='absolute inset-0 flex items-center justify-center z-50 ' style={{ marginTop: topMargin }}>
      <div className='absolute inset-0 bg-white bg-opacity-50 backdrop-blur-sm ' />

      <div className='relative bg-white p-8 rounded-xl shadow-2xl max-w-md w-full mx-4 border border-gray-100'>
        <h2 className='text-1xl text-center font-semibold text-gray-800 mb-4'>Welcome to IATA Document Assistant</h2>

        <p className='text-gray-600 mb-6'>Please select a service to start uploading your documents for processing</p>

        <div className='space-y-4'>
          <button
            onClick={() => onServiceSelect("snowflake")}
            className='w-full py-3 px-4 bg-white border border-gray-300 hover:border-blue-500 hover:text-blue-600 text-gray-700 rounded-lg transition-all transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center space-x-2 shadow-sm'
          >
            <span>Snowflake Service</span>
          </button>

          <button
            onClick={() => onServiceSelect("azure")}
            className='w-full py-3 px-4 bg-white border border-gray-300 hover:border-blue-500 hover:text-blue-600 text-gray-700 rounded-lg transition-all transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center space-x-2 shadow-sm'
          >
            <span>Azure Service</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ServiceSelectionOverlay;

import React, { useEffect, useState } from "react";

const PROCESSING_STEPS = [
  "Sending file to validation service....",
  "Validation in progress...",
  "Summarize the required additional documents...",
  "Almost done with your file validation, it will take just a few more moments...",
];

const STEP_DURATION = 15000; // 15 seconds per step

interface LoadingMessageProps {
  isInitialUpload?: boolean;
}

const LoadingMessage: React.FC<LoadingMessageProps> = ({ isInitialUpload = true }) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const steps = isInitialUpload ? PROCESSING_STEPS : ["Processing your supporting document..."];

  useEffect(() => {
    if (steps.length <= 1) return;

    const interval = setInterval(() => {
      setCurrentStepIndex((prevIndex) => (prevIndex < steps.length - 1 ? prevIndex + 1 : prevIndex));
    }, STEP_DURATION);

    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className='flex items-start gap-3 py-4 px-6 bg-gray-50 rounded-lg'>
      <div className='animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500 mt-1'></div>
      <p className='text-gray-700'>{steps[currentStepIndex]}</p>
    </div>
  );
};

export default LoadingMessage;

import React from "react";
import qatarLogo from "../assets/Qatar-logo.png";
import snowflakeLogo from "../assets/Snowflake_Logo.svg";
import dreamixLogo from "../assets/Dreamix-Logo.png";
import iataLogo from "../assets/IATA-Logo.png";
import infosysLogo from "../assets/Infosys_logo.jpg";

interface HeaderProps {
  isMobileOrTablet: boolean;
  onMenuClick: () => void;
}

export const Header: React.FC<HeaderProps> = ({ isMobileOrTablet, onMenuClick }) => {
  return (
    <header className={`fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-40 ${isMobileOrTablet ? "h-34" : "h-20"}`}>
      <div className={`flex justify-center items-center px-4 relative ${isMobileOrTablet ? "py-4" : "h-20"}`}>
        {isMobileOrTablet && (
          <button onClick={onMenuClick} className='absolute left-4 top-4 p-2 bg-white hover:bg-gray-100 rounded-lg transition-colors'>
            <svg
              xmlns='http://www.w3.org/2000/svg'
              fill='none'
              viewBox='0 0 24 24'
              strokeWidth={1.5}
              stroke='currentColor'
              className='w-6 h-6 text-blue-500'
            >
              <path strokeLinecap='round' strokeLinejoin='round' d='M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5' />
            </svg>
          </button>
        )}

        <div className={`flex items-center justify-center ${isMobileOrTablet ? "flex-col gap-4" : "flex-row gap-12"}`}>
          {isMobileOrTablet ? (
            <div className='flex flex-col gap-4 ml-8'>
              <div className='flex gap-2 justify-center'>
                <div className='w-24 h-14 flex items-center justify-center'>
                  <img src={qatarLogo} alt='Qatar Airways Logo' className='max-h-14 w-auto object-contain' />
                </div>
                <div className='w-24 h-12 flex items-center justify-center'>
                  <img src={iataLogo} alt='IATA Logo' className='max-h-10 w-auto object-contain' />
                </div>
                <div className='w-24 h-16 flex items-center justify-center'>
                  <img src={infosysLogo} alt='Infosys Logo' className='max-h-10 w-auto object-contain' />
                </div>
              </div>
              <div className='flex gap-7 justify-center'>
                <div className='w-28 h-10 flex items-center justify-center'>
                  <img src={snowflakeLogo} alt='Snowflake Logo' className='max-h-8 w-auto object-contain' />
                </div>
                <div className='w-28 h-10 flex items-center justify-center'>
                  <img src={dreamixLogo} alt='Dreamix Logo' className='max-h-8 w-auto object-contain' />
                </div>
              </div>
            </div>
          ) : (
            <>
              <div className='w-32 h-14 flex items-center justify-end'>
                <img src={qatarLogo} alt='Qatar Airways Logo' className='max-h-10 w-auto object-contain' />
              </div>
              <div className='w-32 h-12 flex items-center justify-center'>
                <img src={snowflakeLogo} alt='Snowflake Logo' className='max-h-8 w-auto object-contain' />
              </div>
              <div className='w-32 h-10 flex items-center justify-center'>
                <img src={iataLogo} alt='IATA Logo' className='max-h-10 w-auto object-contain' />
              </div>
              <div className='w-32 h-12 flex items-center justify-center'>
                <img src={dreamixLogo} alt='Dreamix Logo' className='max-h-8 w-auto object-contain' />
              </div>

              <div className='w-32 h-10 flex items-center justify-start'>
                <img src={infosysLogo} alt='Infosys Logo' className='max-h-10 w-auto object-contain' />
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;

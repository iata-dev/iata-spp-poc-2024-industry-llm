import React, { useState } from "react";
import { strings } from "../constants/strings";
import { Conversation, ServiceSource } from "../types";
import ConversationSidebar from "./ConversationSidebar";

interface SidebarProps {
  isMobileOrTablet: boolean;
  isSidebarOpen: boolean;
  onClose: () => void;
  onNewConversation: (service: "azure" | "snowflake") => void;
  conversations: Conversation[];
  activeConversationId: string | null;
  onConversationSelect: (id: string) => void;
  activeService: ServiceSource | null;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isMobileOrTablet,
  isSidebarOpen,
  onClose,
  onNewConversation,
  conversations,
  activeConversationId,
  onConversationSelect,
  activeService,
}) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  return (
    <>
      {isMobileOrTablet && isSidebarOpen && <div className='fixed inset-0 bg-black bg-opacity-50 z-40' onClick={onClose} />}

      <aside
        className={`fixed top-0 left-0 h-full bg-white w-64 border-r border-gray-200 z-50 transition-transform duration-300 ${
          isMobileOrTablet ? (isSidebarOpen ? "translate-x-0" : "-translate-x-full") : "translate-x-0"
        }`}
      >
        {isMobileOrTablet && (
          <>
            <button onClick={onClose} className='absolute top-4 right-4 p-2 bg-white hover:bg-gray-100 rounded-lg transition-colors'>
              <svg
                xmlns='http://www.w3.org/2000/svg'
                fill='none'
                viewBox='0 0 24 24'
                strokeWidth={1.5}
                stroke='currentColor'
                className='w-6 h-6 text-blue-500'
              >
                <path strokeLinecap='round' strokeLinejoin='round' d='M6 18L18 6M6 6l12 12' />
              </svg>
            </button>
            <div className='pt-16' />
          </>
        )}

        <div className='p-4'>
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            disabled={!activeService}
            className='w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors'
          >
            <svg
              xmlns='http://www.w3.org/2000/svg'
              fill='none'
              viewBox='0 0 24 24'
              strokeWidth={1.5}
              stroke='currentColor'
              className='w-5 h-5'
            >
              <path strokeLinecap='round' strokeLinejoin='round' d='M12 4.5v15m7.5-7.5h-15' />
            </svg>
            {strings.buttons.newAwbSubmission}
          </button>
        </div>

        {isDropdownOpen && (
          <div className='absolute left-4 right-4 mt-2 bg-white rounded-lg shadow-lg border border-gray-200 z-50'>
            <button
              onClick={() => {
                onNewConversation("azure");
                setIsDropdownOpen(false);
              }}
              className='w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors rounded-t-lg flex items-center gap-2'
            >
              {strings.buttons.azureService}
            </button>
            <button
              onClick={() => {
                onNewConversation("snowflake");
                setIsDropdownOpen(false);
              }}
              className='w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors rounded-b-lg flex items-center gap-2'
            >
              {strings.buttons.snowflakeService}
            </button>
          </div>
        )}

        <div className='overflow-y-auto h-[calc(100%-5rem)]'>
          {conversations.length > 0 ? (
            <ConversationSidebar
              conversations={conversations}
              activeConversationId={activeConversationId}
              onConversationSelect={onConversationSelect}
            />
          ) : (
            <div className='flex flex-col items-center justify-center p-4 text-center'>
              <svg
                xmlns='http://www.w3.org/2000/svg'
                fill='none'
                viewBox='0 0 24 24'
                strokeWidth={1.5}
                stroke='currentColor'
                className='w-12 h-12 text-gray-400 mb-3'
              >
                <path
                  strokeLinecap='round'
                  strokeLinejoin='round'
                  d='M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z'
                />
              </svg>
              <p className='text-lg font-medium text-gray-600 mb-2'>No Conversations Yet</p>
              <p className='text-gray-500'>Start a new conversation using the button above</p>
            </div>
          )}
        </div>
      </aside>
    </>
  );
};

export default Sidebar;

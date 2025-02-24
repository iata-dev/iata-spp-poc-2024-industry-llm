import { useState, useEffect } from "react";

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed" }>;
}

interface PWAPromptProps {
  isMobileOrTablet?: boolean;
}

export function PWAPrompt({ isMobileOrTablet = false }: PWAPromptProps) {
  const [installPrompt, setInstallPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      if (isMobileOrTablet) {
        setInstallPrompt(e as BeforeInstallPromptEvent);
        setShowPrompt(true);
      }
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
    };
  }, [isMobileOrTablet]);

  const handleInstallClick = async () => {
    if (!installPrompt) return;

    await installPrompt.prompt();
    const { outcome } = await installPrompt.userChoice;

    if (outcome === "accepted") {
      setShowPrompt(false);
    }
  };

  if (!showPrompt) return null;

  return (
    <div className={`fixed bottom-4 left-4 right-4 bg-white p-4 rounded-lg shadow-lg md:max-w-md ${isMobileOrTablet ? "" : "ml-64"}`}>
      <div className='flex items-center justify-between'>
        <div className='flex-1'>
          <h3 className='text-lg font-semibold'>Install App</h3>
          <p className='text-sm text-gray-600'>Install this app on your device for quick and easy access</p>
        </div>
        <div className='flex gap-2 ml-4'>
          <button onClick={() => setShowPrompt(false)} className='px-3 py-1.5 text-sm text-gray-600 hover:text-gray-800'>
            Not now
          </button>
          <button onClick={handleInstallClick} className='px-3 py-1.5 text-sm bg-blue-500 text-white rounded-md hover:bg-blue-600'>
            Install
          </button>
        </div>
      </div>
    </div>
  );
}

export default PWAPrompt;

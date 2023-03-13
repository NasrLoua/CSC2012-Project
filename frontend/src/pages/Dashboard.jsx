import React from 'react';
import ScanningSection from '../components/ScanningSection';
import ResultSection from '../components/ResultSection';

export default function Dashboard() {
    return (
      <div className="flex flex-row h-screen">
        <div className="w-full md:w-1/2 px-4 py-2 ml-10">
          <ScanningSection />
        </div>
        <div className="w-full md:w-1/2 px-4 py-2">
          <ResultSection />
        </div>
      </div>
    );
  }
import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { extractFeatures } from '../featureExtractor';

const Results = () => {
    const location = useLocation();
    const { boqText, selectedCity } = location.state || {}; // Get BOQ text and selected city from state

    const [mlResults, setMlResults] = useState(null);
    const [loading, setLoading] = useState(true);

    // Extract features from the BOQ text
    const extractedFeatures = extractFeatures(boqText || '');

    useEffect(() => {
        const fetchMlResults = async () => {
            setLoading(true);
            try {
                const response = await fetch('/api/ml-results', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ city: selectedCity }),
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch ML results');
                }
                const data = await response.json();
                console.log('ML Results:', data); 
                setMlResults(data);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        fetchMlResults();
    }, [selectedCity]);

    return (
        <div className="p-4 ml-[260px] font-poppins top-50">
            <h2 className="text-2xl font-bold mb-4">Results</h2>
            <div className="bg-gray-100 p-4 rounded">
                <h3 className="font-bold">Entered BOQ:</h3>
                <p className="mb-4">{boqText || "No BOQ text provided."}</p>

                <h3 className="font-bold mt-4">Extracted Features:</h3>
                <ul className="list-none">
                    {Object.entries(extractedFeatures).map(([key, value]) => {
                        const formattedKey = key.replace(/([a-z])([A-Z])/g, '$1 $2');
                        return (
                            <li key={key} className="mb-2">
                                <strong>{formattedKey}:</strong> {value !== null ? value : "null"}
                            </li>
                        );
                    })}
                </ul>

                {loading ? (
                    <p>Loading ML results...</p>
                ) : (
                    mlResults && (
                        <div>
                            <h3 className="font-bold mt-4">ML Results:</h3>
                            <p>Distance to Gurgaon: {mlResults.distance} km</p>
                            <h4 className="font-bold mt-2">Top Vendors:</h4>
                            <ul>
                                {mlResults.top_vendors.map((vendor, index) => (
                                    <li key={index}>
                                        <strong>{vendor['FACADE VENDOR']}</strong> - Location: {vendor['Factory Location']} - Ranking Score: {vendor['Ranking_Score']}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )
                )}
            </div>
        </div>
    );
};

export default Results;

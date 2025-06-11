// Quick test script to verify our analysis API
async function testAnalysis() {
  console.log('Testing brand analysis API...');
  
  try {
    const response = await fetch('http://localhost:3003/api/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        brands: ['wolterskluwer.com', 'elsevier.com', 'openevidence.com']
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    console.log('\n📊 Analysis Results:');
    console.log('Total brands:', data.brands?.length || 0);
    console.log('Industry:', data.industry);
    console.log('Average score:', data.summary?.averageScore || 'N/A');
    
    console.log('\n🏢 Brand Results:');
    data.brands?.forEach((brand, index) => {
      console.log(`${index + 1}. ${brand.name}: ${brand.score}/100`);
      if (brand.error) {
        console.log(`   Error: ${brand.error}`);
      } else {
        console.log(`   Industry: ${brand.overview?.industry || 'N/A'}`);
        console.log(`   Visual: ${brand.visual?.logo ? 'Logo found' : 'No logo'}, ${brand.visual?.colors?.length || 0} colors`);
      }
    });
    
    console.log('\n🎯 Competitive Insights:');
    data.competitiveInsights?.forEach((insight, index) => {
      console.log(`${index + 1}. ${insight}`);
    });
    
    console.log('\n✅ Test completed successfully!');
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    console.error('Full error:', error);
  }
}

testAnalysis();
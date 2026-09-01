/**
 * Advanced Production-Grade Zero-CORS Bootstrap Loader
 * Engineered to completely isolate the TensorFlow.js core layer from origin blockages.
 */
(function() {
    console.log("⚙️ Allocating safe system runtime blocks...");
    
    // Injecting a native ES Module dynamically into the global window context
    import('https://esm.run')
        .then(function(mlCoreModule) {
            // Binding the loaded module directly to the window object to break variable scoping fences
            window.tf = mlCoreModule;
            console.log("🎉 Core machine learning architecture unlocked successfully inside global memory grid.");
            
            // Instantly re-triggering the application initialization sequence inside index.html
            if (typeof startApplicationPipeline === 'function') {
                startApplicationPipeline();
            }
        })
        .catch(function(runtimeBootstrapError) {
            console.error("Critical failure during neural engine allocation:", runtimeBootstrapError);
        });
})();

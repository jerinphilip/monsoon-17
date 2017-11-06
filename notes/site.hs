--------------------------------------------------------------------------------
{-# LANGUAGE OverloadedStrings #-}
import           Data.Monoid (mappend)
import           Hakyll
import           System.Directory
import           System.FilePath
import           Control.Monad
import           Data.List (isInfixOf)
import qualified Data.Set as S
import           Text.Pandoc.Options



--------------------------------------------------------------------------------

getJournal :: String -> IO [String]
getJournal root = do
    fs <- listDirectory root
    let prependPath x = root </> x
    return (map prependPath fs)

htRoute = composeRoutes (gsubRoute "htaccess" (const ".htaccess")) idRoute

    
    
main :: IO ()
main = do
    projects <- getJournal "journal"
    hakyll $ do
        match "static/images/*" $ do
            route   idRoute
            compile copyFileCompiler

        match "static/css/*" $ do
            route   idRoute
            compile compressCssCompiler
        
        match "static/js/*" $ do
            route idRoute
            compile copyFileCompiler

        match "**/htaccess" $ do
            route htRoute
            compile copyFileCompiler

        match (fromList ["about.rst", "contact.markdown"]) $ do
            route $ setExtension "html"
            compile $ pandocMathCompiler
                >>= loadAndApplyTemplate "templates/layout.html" defaultContext
                >>= relativizeUrls
                >>= removeIndexHtml

        match "posts/*" $ do
            route $ setExtension "html"
            compile $ pandocMathCompiler
                >>= loadAndApplyTemplate "templates/post.html"    datedCtx 
                >>= loadAndApplyTemplate "templates/layout.html" datedCtx
                >>= relativizeUrls
                >>= removeIndexHtml

        create ["archive.html"] $ do
            route idRoute
            compile $ do
                posts <- recentFirst =<< loadAll "posts/*"
                let archiveCtx =
                        listField "posts" datedCtx (return posts) `mappend`
                        constField "title" "Archives"            `mappend`
                        defaultContext

                makeItem ""
                    >>= loadAndApplyTemplate "templates/archive.html" archiveCtx
                    >>= loadAndApplyTemplate "templates/layout.html" archiveCtx
                    >>= relativizeUrls
                    >>= removeIndexHtml

        match "index.html" $ do
            route idRoute
            compile $ do
                posts <- recentFirst =<< loadAll "posts/*"
                projects <- loadAll "journal/*/index.md"
                let indexCtx =
                        listField "posts" datedCtx (return posts)            `mappend`
                        listField "projects" defaultContext (return projects)`mappend`
                        constField "title" "About"                            `mappend`
                        defaultContext

                getResourceBody
                    >>= applyAsTemplate indexCtx
                    >>= loadAndApplyTemplate "templates/layout.html" indexCtx
                    >>= relativizeUrls
                    >>= removeIndexHtml

        match "templates/*" $ compile templateBodyCompiler

        match "journal/**/notes/**.md" $ do
            route $ setExtension "html"
            compile $ pandocMathCompiler
                >>= loadAndApplyTemplate "templates/layout.html" defaultContext
                >>= relativizeUrls
                >>= removeIndexHtml

        match "journal/**/updates/**md" $ do
            compile $ pandocMathCompiler

        -- match "journal/**/index.md" $ do
        --     compile $ pandocMathCompiler

        forM_ projects $ \project -> do
            let notesPath = project </> "notes/"
            let updatesPath = project </> "updates/"
            let identifier = fromFilePath (project </> "index.html")
            let projectPattern = fromGlob (project </> "index.md")
            -- create [identifier]  $ do
            match projectPattern $ do
                route $ setExtension "html"
                compile $ do
                   notes    <- loadAll (fromGlob (notesPath </> "**.md"))
                   -- meta     <- loadAll (fromGlob (project </> "index.md"))
                   updates  <- liftM (take 2) . recentFirst =<< loadAll (fromGlob (updatesPath </> "**.md"))
                   let projectCtx =
                           listField "updates" datedCtx (return updates)      `mappend`
                           listField "notes" defaultContext (return notes)    `mappend`
                           constField "updates-url" ("/" </> project </> "updates/")  `mappend`
                           -- listField "meta" defaultContext (return meta)    `mappend`
                           defaultContext

                   -- makeItem ""
                   pandocMathCompiler
                       >>= loadAndApplyTemplate "templates/project.html"  projectCtx
                       >>= loadAndApplyTemplate "templates/layout.html"   projectCtx
                       >>= relativizeUrls
                       >>= removeIndexHtml

            let notesIdentifier = fromFilePath $ updatesPath </> "index.html"
            create [notesIdentifier] $ do
                route idRoute
                compile $ do
                   updates  <- chronological =<< loadAll (fromGlob (updatesPath </> "**.md"))
                   let updateCtx = 
                        listField "updates" datedCtx (return updates) `mappend`
                        constField "title" "Update Archives" `mappend`
                        defaultContext
                   -- let updateCtx = defaultContext
                   makeItem ""
                        >>= loadAndApplyTemplate "templates/updates.html" updateCtx
                        >>= loadAndApplyTemplate "templates/layout.html" updateCtx
                        >>= relativizeUrls
                        >>= removeIndexHtml


--------------------------------------------------------------------------------
datedCtx :: Context String
datedCtx =
    dateField "date" "%B %e, %Y" `mappend`
    dateField "date-hash" "%d-%m-%0Y" `mappend`
    defaultContext


-- replace url of the form foo/bar/index.html by foo/bar
removeIndexHtml :: Item String -> Compiler (Item String)
removeIndexHtml item = return $ fmap (withUrls removeIndexStr) item
  where
    removeIndexStr :: String -> String
    removeIndexStr url = case splitFileName url of
        (dir, "index.html") | isLocal dir -> dir
        _                                 -> url
        where isLocal uri = not (isInfixOf "://" uri)

pandocMathCompiler =
    let mathExtensions = [Ext_tex_math_dollars, Ext_tex_math_double_backslash,
                          Ext_latex_macros]
        defaultExtensions = writerExtensions defaultHakyllWriterOptions
        newExtensions = foldr S.insert defaultExtensions mathExtensions
        writerOptions = defaultHakyllWriterOptions {
                          writerExtensions = newExtensions,
                          writerHTMLMathMethod = MathJax ""
                        }
    in pandocCompilerWith defaultHakyllReaderOptions writerOptions


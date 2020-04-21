import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

public class DataAnalyzer
{
    List<Document> positiveReviews;
    List<Document> negativeReviews;
    int minDocLengthBySentence;
    int avgDocLengthBySentence;
    int maxDocLengthBySentence;
    int minDocLengthByToken;
    int avgDocLengthByToken;
    int maxDocLengthByToken;
    int avgSentenceLengthByToken;
    
    public DataAnalyzer()
    {
        positiveReviews = new ArrayList<>();
        negativeReviews = new ArrayList<>();
        minDocLengthBySentence = Integer.MAX_VALUE;
        minDocLengthByToken = Integer.MAX_VALUE;
        maxDocLengthBySentence = Integer.MIN_VALUE;
        maxDocLengthByToken = Integer.MIN_VALUE;
    }

    public void loadReviewData(String posReviewFilePath, String negReviewFilePath)
    {
        loadPositiveReviews(posReviewFilePath);
        loadNegativeReviews(negReviewFilePath);
    }

    public void loadPositiveReviews(String filePath)
    {
        final File folder = new File(filePath);
        for (File entry: folder.listFiles())
        {
            if (entry.isFile())
            {
                String document = fileToString(entry.getAbsolutePath());
                Document positiveReview = new Document(document);
                positiveReviews.add(positiveReview);
            }
        }
    }

    public void loadNegativeReviews(String filePath)
    {
        final File folder = new File(filePath);
        for (File entry: folder.listFiles())
        {
            if (entry.isFile())
            {
                String document = fileToString(entry.getAbsolutePath());
                Document negativeReview = new Document(document);
                negativeReviews.add(negativeReview);
            }
        }
    }

    public static String fileToString(String filePath)
    {
        StringBuilder sb = new StringBuilder();

        try
        {
            BufferedReader bufferedReader = new BufferedReader(new FileReader(filePath));
            String inputLine = bufferedReader.readLine();
        
            while (inputLine != null)
            {
                sb.append(inputLine);
                sb.append("\n");
                inputLine = bufferedReader.readLine();
            }
            bufferedReader.close();
        }
        catch(Exception e)
        {
            System.out.println(e.getMessage());
        }

        return sb.toString();
    }

    public void calculateDocumentStatistics()
    {
        calculateTokenStatistics();
        calculateSentenceStatistics();
    }

    public void calculateTokenStatistics()
    {
        if (positiveReviews.size() != 0 || negativeReviews.size() != 0)
        {
            int totalNumberOfTokens = 0;
            for (Document doc: positiveReviews)
            {
                int numberOfTokens = doc.getNumberOfTokens();
                totalNumberOfTokens += numberOfTokens;
                minDocLengthByToken = Math.min(minDocLengthByToken, numberOfTokens);
                maxDocLengthByToken = Math.max(maxDocLengthByToken, numberOfTokens);
            }
            for (Document doc: negativeReviews)
            {
                int numberOfTokens = doc.getNumberOfTokens();
                totalNumberOfTokens += numberOfTokens;
                minDocLengthByToken = Math.min(minDocLengthByToken, numberOfTokens);
                maxDocLengthByToken = Math.max(maxDocLengthByToken, numberOfTokens);
            }
            avgDocLengthByToken = totalNumberOfTokens / (positiveReviews.size() + negativeReviews.size());
        }
    }

    public void calculateSentenceStatistics()
    {
        if (positiveReviews.size() != 0 || negativeReviews.size() != 0)
        {
            int totalNumOfSentences = 0;
            for (Document doc: positiveReviews)
            {
                int numberOfSentences = doc.getNumberOfSentences();
                avgSentenceLengthByToken += doc.getAvgSentenceLengthByToken();
                totalNumOfSentences += numberOfSentences;
                minDocLengthBySentence = Math.min(minDocLengthBySentence, numberOfSentences);
                maxDocLengthBySentence = Math.max(maxDocLengthBySentence, numberOfSentences);
            }
            for (Document doc: negativeReviews)
            {
                int numberOfSentences = doc.getNumberOfSentences();
                avgSentenceLengthByToken += doc.getAvgSentenceLengthByToken();
                totalNumOfSentences += numberOfSentences;
                minDocLengthBySentence = Math.min(minDocLengthBySentence, numberOfSentences);
                maxDocLengthBySentence = Math.max(maxDocLengthBySentence, numberOfSentences);
            }
            avgDocLengthBySentence = totalNumOfSentences / (positiveReviews.size() + negativeReviews.size());
            avgSentenceLengthByToken /= (positiveReviews.size() + negativeReviews.size());
        }
    }

    public void printStatistics()
    {
        int numberOfPosReviews = positiveReviews.size();
        int numberOfNegReviews = negativeReviews.size();
        int totalNumberOfDocuments = numberOfPosReviews + numberOfNegReviews;
        System.out.printf("Total number of documents in collection: %d (%d positive, %d negative)\n\n", totalNumberOfDocuments, numberOfPosReviews, numberOfNegReviews);
        System.out.printf("Sentence Data\n-------------\n");
        System.out.printf("Minimum document length by number of sentences: %d\n", minDocLengthBySentence);
        System.out.printf("Maximum document length by number of sentences: %d\n", maxDocLengthBySentence);
        System.out.printf("Average document length by number of sentences: %d\n\n", avgDocLengthBySentence);
        System.out.printf("Token Data\n-------------\n");
        System.out.printf("Minimum document length by number of tokens: %d\n", minDocLengthByToken);
        System.out.printf("Maximum document length by number of tokens: %d\n", maxDocLengthByToken);
        System.out.printf("Average document length by number of tokens: %d\n\n", avgDocLengthByToken);
        System.out.printf("Average sentence length by number of tokens: %d\n\n", avgSentenceLengthByToken);
    }

    public static void main(String[] args)
    {
        if (args.length > 1)
        {
            DataAnalyzer dataAnalyzer = new DataAnalyzer();
            dataAnalyzer.loadReviewData(args[0], args[1]);
            dataAnalyzer.calculateDocumentStatistics();
            dataAnalyzer.printStatistics();
        }
        else
        {
            System.out.printf("usage: java DataAnalyzer <positive_review_folder> <negative_review_folder>\n");
        }
    }
}

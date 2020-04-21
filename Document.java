import java.util.HashSet;
import java.util.Set;

public class Document
{
    String content;
    int numberOfSentences;
    int numberOfTokens;

    public Document(String content)
    {
        this.content = content;
        calculateNumberOfSentences();
        calculateNumberOfTokens();
    }

    public void setContent(String content)
    {
        this.content = content;
    }

    public String getContent()
    {
        return this.content;
    }

    public void setNumberOfSentences(int numberOfSentences)
    {
        this.numberOfSentences = numberOfSentences;
    }

    public int getNumberOfSentences()
    {
        return this.numberOfSentences;
    }

    public void setNumberOfTokens(int numberOfTokens)
    {
        this.numberOfTokens = numberOfTokens;
    }

    public int getNumberOfTokens()
    {
        return this.numberOfTokens;
    }

    public int getNumberOfDistinctTokens()
    {
        Set<String> tokens = new HashSet<>();
        for (String s: this.content.split("\n"))
        {
            for (String token: s.split(" "))
            {
                tokens.add(token);
            }
        }
        return tokens.size();
    }

    public int getAvgSentenceLengthByToken()
    {
        if (numberOfSentences > 0)
        {
            return numberOfTokens / numberOfSentences;
        }
        return 0;
    }

    public void calculateNumberOfSentences()
    {
        this.numberOfSentences = this.content.split("\n").length;
    }

    public void calculateNumberOfTokens()
    {
        int numberOfTokens = 0;
        for (String s: this.content.split("\n"))
        {
            numberOfTokens += s.split(" ").length;
        }
        this.numberOfTokens = numberOfTokens;
    }
}